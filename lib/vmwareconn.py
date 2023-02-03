import logging
import ssl
from pyVmomi import vim, vmodl  # type: ignore
from pyVim import connect

from .asset_cache import AssetCache

MAX_CONN_AGE = 900


def get_alarms(ip4, username, password):
    content = _get_content(ip4, username, password)
    return content.rootFolder.triggeredAlarmState


def get_data(ip4, username, password, obj_type, properties):
    content = _get_content(ip4, username, password)
    data = _query_view(
        content=content,
        obj_type=obj_type,
        properties=properties)

    return data


def get_perf(ip4, username, password, obj_type, metrics):
    content = _get_content(ip4, username, password)
    view_ref = content.viewManager.CreateContainerView(
        container=content.rootFolder, type=[obj_type], recursive=True)

    perf_manager = content.perfManager
    counters_lk = {c.key: c for c in perf_manager.perfCounter}

    results = {}
    for child in view_ref.view:
        available = perf_manager.QueryAvailablePerfMetric(entity=child)

        metric_id = [
            vim.PerformanceManager.MetricId(counterId=m.counterId,
                                            instance=m.instance)
            for m in available
            if m.counterId in counters_lk and (
                counters_lk[m.counterId].groupInfo.key,
                counters_lk[m.counterId].nameInfo.key) in metrics
        ]
        if len(metric_id) == 0:
            # nothing to query
            continue

        spec = vim.PerformanceManager.QuerySpec(intervalId=20, maxSample=15,
                                                entity=child,
                                                metricId=metric_id)
        results[child.config.instanceUuid] = result = {m: {} for m in metrics}
        for stat in perf_manager.QueryStats(querySpec=[spec]):
            for val in stat.value:
                counter = counters_lk[val.id.counterId]
                path = counter.groupInfo.key, counter.nameInfo.key
                instance = val.id.instance
                value = val.value
                result[path][instance] = value

    view_ref.Destroy()
    return results


def drop_connnection(host):
    conn, _ = AssetCache.get_value((host, 'connection'))
    if conn:
        AssetCache.drop((host, 'connection'))
        conn._stub.DropConnections()


def _get_content(host, username, password):
    conn, expired = AssetCache.get_value((host, 'connection'))
    if expired:
        conn._stub.DropConnections()
    elif conn:
        return conn.RetrieveContent()

    conn = _get_connection(host, username, password)
    if not conn:
        raise ConnectionError('Unable to connect')
    AssetCache.set_value((host, 'connection'), conn, MAX_CONN_AGE)
    return conn.RetrieveContent()


def _get_connection(host, username, password):
    logging.info(f'CONNECTING to {host}')
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    return connect.SmartConnect(
        host=host,
        user=username,
        pwd=password,
        sslContext=context,
        connectionPoolTimeout=10)


def _query_view(content, obj_type, properties):
    view_ref = content.viewManager.CreateContainerView(
        container=content.rootFolder, type=[obj_type], recursive=True)
    collector = content.propertyCollector

    obj_spec = vmodl.query.PropertyCollector.ObjectSpec()
    obj_spec.obj = view_ref
    obj_spec.skip = True

    # Create a traversal specification to identify the
    # path for collection
    traversal_spec = vmodl.query.PropertyCollector.TraversalSpec()
    traversal_spec.name = 'traverseEntities'
    traversal_spec.path = 'view'
    traversal_spec.skip = False
    traversal_spec.type = view_ref.__class__
    obj_spec.selectSet = [traversal_spec]

    # Identify the properties to the retrieved
    property_spec = vmodl.query.PropertyCollector.PropertySpec()
    property_spec.type = obj_type
    property_spec.all = False

    property_spec.pathSet = properties

    # Add the object and property specification to the
    # property filter specification
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = [obj_spec]
    filter_spec.propSet = [property_spec]

    # Retrieve properties
    return collector.RetrieveContents([filter_spec])
