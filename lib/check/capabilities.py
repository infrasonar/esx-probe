from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
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
        {
            'name': name,
            'capability': getattr(prop.val, name)
        }
        for item in result
        for prop in item.propSet
        for name in prop.val._propInfo
        if isinstance(getattr(prop.val, name, None), bool)
    ]

    return {
        'capability': capabilities
    }
