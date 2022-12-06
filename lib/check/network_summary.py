from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict
from ..vmwarequery import vmwarequery


async def check_network_summary(
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
        prop_val_to_dict(prop.val)
        for item in result
        for prop in item.propSet
    ]

    return {
        'network': networks
    }
