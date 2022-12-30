from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import datetime_to_timestamp
from ..vmwarequery import vmwarequery


async def check_datastore(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.Datastore,
        ['info', 'summary'],
    )
    datastore_out = []
    vmfs_out = []
    nas_out = []
    for item in result:
        info, summary = item.propSet

        datastore = {
            'name': summary.val.name,  # str
            'accessible':  summary.val.accessible,
            'capacity': summary.val.capacity,  # int
            'freeSpace': summary.val.freeSpace,  # int
            'maintenanceMode': summary.val.maintenanceMode,  # str/null
            'multipleHostAccess': summary.val.multipleHostAccess,  # bool/null
            'type': summary.val.type,  # str
            'uncommitted': summary.val.uncommitted,  # int/null
            'url': summary.val.url,  # str
            'maxFileSize': info.val.maxFileSize,  # int
            'maxMemoryFileSize': getattr(
                info.val, 'maxMemoryFileSize', None),  # int/null
            'maxPhysicalRDMFileSize': getattr(
                info.val, 'maxPhysicalRDMFileSize', None),  # int/null
            'maxVirtualDiskCapacity': getattr(
                info.val, 'maxVirtualRDMFileSize', None),  # int/null
            'maxVirtualRDMFileSize': getattr(
                info.val, 'maxVirtualRDMFileSize', None),  # int/null

        }
        datastore_out.append(datastore)

        dt = getattr(info.val, 'timestamp', None)
        if dt is not None:
            datastore['timestamp'] = datetime_to_timestamp(dt)
        vmfs = getattr(info.val, 'vmfs', None)
        if vmfs is not None:
            datastore['vmfs'] = vmfs.name
            vmfs_out.append({
                'name': vmfs.name,
                'datastore': datastore['name'],
                'blockSizeMb': vmfs.blockSizeMb,
                'blockSize': vmfs.blockSize,
                'unmapGranularity': vmfs.unmapGranularity,  # int/null
                'unmapPriority': vmfs.unmapPriority,  # str/null
                'unmapBandwidthSpec': vmfs.unmapBandwidthSpec,
                'maxBlocks': vmfs.maxBlocks,
                'majorVersion': vmfs.majorVersion,
                'uuid': vmfs.uuid,
                'version': vmfs.version,
                'vmfsUpgradable': vmfs.vmfsUpgradable,
                'ssd': vmfs.ssd,
                'local': vmfs.local,
                'scsiDiskType': vmfs.scsiDiskType,
            })
        nas = getattr(info.val, 'nas', None)
        if nas is not None:
            nas_out.append({
                'name': nas.name,
                'datastore': datastore['name'],
                'protocolEndpoint': nas.protocolEndpoint,
                'remoteHost': nas.remoteHost,
                'remotePath': nas.remotePath,
                # 'securityType': nas.securityType,
                # 'userName': nas.userName,
            })

    return {
        'datastore': datastore_out,
        'vmfs': vmfs_out,
        'nas': nas_out,
    }
