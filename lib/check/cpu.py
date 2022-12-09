from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


async def check_cpu(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['hardware.cpuPkg'],
    )

    cpus = [
        {
            'name': str(prop_val.index),
            'busHz': prop_val.busHz,  # int
            'description': prop_val.description,  # str
            'hz': prop_val.hz,  # int
            'index': prop_val.index,  # int
            'vendor': prop_val.vendor,  # str
        }
        for item in result
        for prop in item.propSet
        for prop_val in prop.val
    ]

    return {
        'cpu': cpus
    }
