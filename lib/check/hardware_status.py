from itertools import chain
from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


async def check_hardware_status(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['runtime.healthSystemRuntime.hardwareStatusInfo'],
    )

    hardware_status = [
        {
            'name': si.name,
            'status': si.status.key,
        }
        for item in result
        for prop in item.propSet
        for si in chain(
             prop.val.memoryStatusInfo,
             prop.val.cpuStatusInfo,
             prop.val.storageStatusInfo,
        )
    ]

    return {
        'hardwareStatus': hardware_status
    }
