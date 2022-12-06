from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
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
        {
            'name': prop_val.id,  # str
            'classId': prop_val.classId,  # int
            'deviceId': prop_val.deviceId,  # int
            'deviceName': prop_val.deviceName,  # str
            'parentBridge': prop_val.parentBridge,  # str/null
            'subDeviceId': prop_val.subDeviceId,  # int
            'subVendorId': prop_val.subVendorId,  # int
            'vendorId': prop_val.vendorId,  # int
            'vendorName': prop_val.vendorName,  # str
        }
        for item in result
        for prop in item.propSet
        for prop_val in prop.val
    ]

    return {
        'pci': pcis
    }
