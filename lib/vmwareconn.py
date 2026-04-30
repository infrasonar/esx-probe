import logging
import ssl
from pyVmomi import vim, vmodl  # type: ignore
from pyVim import connect

from .asset_cache import AssetCache

MAX_CONN_AGE = 900


def get_content(ip4: str, username: str, password: str):
    conn = _get_conn(ip4, username, password)
    content = conn.RetrieveContent()
    return content


def get_data(ip4: str, username: str, password: str,
             obj_type: type[vim.ManagedEntity], properties: list[str]):
    conn = _get_conn(ip4, username, password)
    content = conn.RetrieveContent()
    data = _query_view(
        content=content,
        obj_type=obj_type,
        properties=properties)

    return data


def drop_connnection(host: str):
    conn, _ = AssetCache.get_value((host, 'connection'))
    if conn:
        AssetCache.drop((host, 'connection'))
        conn._stub.DropConnections()  # type: ignore


def _get_conn(host: str, username: str, password: str):
    conn, expired = AssetCache.get_value((host, 'connection'))
    if conn:
        if expired:
            conn._stub.DropConnections()  # type: ignore
        else:
            return conn

    conn = _get_connection(host, username, password)
    if not conn:
        raise ConnectionError('Unable to connect')
    AssetCache.set_value((host, 'connection'), conn, MAX_CONN_AGE)
    return conn


def _get_connection(host: str, username: str, password: str):
    logging.info(f'CONNECTING to {host}')
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    return connect.SmartConnect(
        host=host,
        user=username,
        pwd=password,
        sslContext=context,
        connectionPoolTimeout=10)


def _query_view(content: vim.ServiceInstanceContent,
                obj_type: type[vim.ManagedEntity], properties: list[str]):
    view_ref = content.viewManager.CreateContainerView(  # type: ignore
        container=content.rootFolder, type=[obj_type], recursive=True)
    collector = content.propertyCollector

    obj_spec = vmodl.query.PropertyCollector.ObjectSpec()
    obj_spec.obj = view_ref
    obj_spec.skip = True

    # Create a traversal specification to identify the
    # path for collection
    traversal_spec = \
        vmodl.query.PropertyCollector.TraversalSpec()
    traversal_spec.name = 'traverseEntities'
    traversal_spec.path = 'view'
    traversal_spec.skip = False
    traversal_spec.type = view_ref.__class__
    obj_spec.selectSet = [traversal_spec]

    # Identify the properties to the retrieved
    property_spec = \
        vmodl.query.PropertyCollector.PropertySpec()
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


# NOTE type ignore
# missing import in pyVmomi.vmodl.__init__.pyi
