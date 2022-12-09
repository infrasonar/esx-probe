import time
from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import datetime_to_timestamp
from ..vmwarequery import vmwarequery


async def check_datastore_summary(
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
            'datastore': summary.val.datastore,
            'name': summary.val.name,
            'url': summary.val.url,
            'capacity': summary.val.capacity,
            'freeSpace': summary.val.freeSpace,
            'uncommitted': summary.val.uncommitted,
            'multipleHostAccess': summary.val.multipleHostAccess,
            'type': summary.val.type,
            'maintenanceMode': summary.val.maintenanceMode,
            'maxPhysicalRDMFileSize': getattr(
                info.val, 'maxPhysicalRDMFileSize', None),
            'maxVirtualRDMFileSize': getattr(
                info.val, 'maxVirtualRDMFileSize', None),

        }
        datastore_out.append(datastore)

        dt = getattr(info.val, 'timestamp', None)
        if dt is not None:
            datastore['timestamp'] = ts = datetime_to_timestamp(dt)
            datastore['age'] = time.time() - ts
        vmfs = getattr(info.val, 'vmfs', None)
        if vmfs is not None:
            vmfs_out.append({
                'name': datastore['name'],
                'datastore': datastore['datastore'],
                'blockSizeMb': vmfs.blockSizeMb,
                'blockSize': vmfs.blockSize,
                'unmapGranularity': vmfs.unmapGranularity,
                'unmapPriority': vmfs.unmapPriority,
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
                'name': datastore['name'],
                'datastore': datastore['datastore'],
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
