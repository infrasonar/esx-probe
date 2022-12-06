import logging
import ssl
from pyVmomi import vmodl  # type: ignore
from pyVim import connect
from requests.exceptions import ConnectionError

from .asset_cache import AssetCache

MAX_CONN_AGE = 900


def get_data(ip4, username, password, obj_type, properties):
    content = _get_content(ip4, username, password)
    data = _query_view(
        content=content,
        obj_type=obj_type,
        properties=properties)

    return data


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
    logging.info('CONNECTING to {}'.format(host))
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
