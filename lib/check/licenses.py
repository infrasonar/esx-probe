from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


async def check_licenses(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['licensableResource'],
    )

    licenses = [
        {
            'name': license.key,
            'value': license.value
        }
        for item in result
        for prop in item.propSet
        for license in prop.val.resource
    ]

    return {
        'licensableResource': licenses
    }
