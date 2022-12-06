import time
from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict, datetime_to_timestamp
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
            **prop_val_to_dict(info.val),
            **prop_val_to_dict(summary.val),
        }
        datastore_out.append(datastore)

        dt = getattr(info.val, 'timestamp', None)
        if dt is not None:
            datastore['timestamp'] = ts = datetime_to_timestamp(dt)
            datastore['age'] = time.time() - ts
        vmfs = getattr(info.val, 'vmfs', None)
        if vmfs is not None:
            vmfs_out.append(prop_val_to_dict(vmfs, datastore['name']))
        nas = getattr(info.val, 'nas', None)
        if nas is not None:
            nas_out.append(prop_val_to_dict(nas, datastore['name']))

    return {
        'datastore': datastore_out,
        'vmfs': vmfs_out,
        'nas': nas_out,
    }
