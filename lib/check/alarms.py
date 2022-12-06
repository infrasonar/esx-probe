from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict
from ..vmwarequery import vmwarequery


async def check_alarms(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['triggeredAlarmState'],
    )

    alarms = [
        {
            **prop_val_to_dict(alarm, item_name=str(alarm.key)),
            'entityName': alarm.entity.name,
            'alarmInfo': alarm.alarm.info.name,
            'alarmDesc': alarm.alarm.info.description,
        }
        for item in result
        for prop in item.propSet
        for alarm in prop.val
    ]

    return {
        'alarms': alarms
    }
