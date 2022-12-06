from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict
from ..vmwarequery import vmwarequery


async def check_pci(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['hardware.pciDevice'],
    )

    pcis = [
        prop_val_to_dict(prop_val, item_name=str(prop_val.id))
        for item in result
        for prop in item.propSet
        for prop_val in prop.val
    ]

    return {
        'pci': pcis
    }
