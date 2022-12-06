from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_value_list
from ..vmwarequery import vmwarequery


async def check_capabilities(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['capability'],
    )

    capabilities = [
        val
        for item in result
        for prop in item.propSet
        for val in prop_val_to_value_list(
            prop.val, value_name='capability')
    ]

    return {
        'capability': capabilities
    }
