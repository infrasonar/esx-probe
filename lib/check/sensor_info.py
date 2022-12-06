from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict
from ..vmwarequery import vmwarequery


async def check_sensor_info(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['runtime.healthSystemRuntime.systemHealthInfo.numericSensorInfo'],
    )

    sensors = [
        {
            **prop_val_to_dict(prop_val),
            'name': prop_val.name,
            'healthState': prop_val.healthState.key,
            'readingValue': prop_val.currentReading * (
                10 ** prop_val.unitModifier),
        }
        for item in result
        for prop in item.propSet
        for prop_val in prop.val
    ]

    return {
        'sensor': sensors
    }
