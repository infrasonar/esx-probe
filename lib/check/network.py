from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


async def check_network(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.Network,
        ['summary'],
    )

    networks = [
        {
            'name': prop.val.name,  # str
            'accessible': prop.val.accessible,  # bool
            'ipPoolId': prop.val.ipPoolId,  # int/null
            'ipPoolName': prop.val.ipPoolName,  # str
        }
        for item in result
        for prop in item.propSet
    ]

    return {
        'network': networks
    }
