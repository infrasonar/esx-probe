from libprobe.asset import Asset
from ..utils import datetime_to_timestamp
from ..vmwarequery import vmwarequery_content


async def check_alarms(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    content = await vmwarequery_content(
        asset,
        asset_config,
        check_config,
    )

    alarms = [
        # vim.alarm.AlarmState
        {
            'name': alarm.key,  # str
            'entityName': alarm.entity.name,  # str
            'alarmInfo': alarm.alarm.info.name,  # str
            'alarmDesc': alarm.alarm.info.description,  # str
            'acknowledged': alarm.acknowledged,  # bool
            'acknowledgedByUser': alarm.acknowledgedByUser,  # str/null
            'acknowledgedTime':
                datetime_to_timestamp(alarm.acknowledgedTime),  # int/null
            'eventKey': alarm.eventKey,  # int/null
            'overallStatus': alarm.overallStatus,  # str
            'time': datetime_to_timestamp(alarm.time),  # int
        }
        for alarm in content.rootFolder.triggeredAlarmState
    ]

    return {
        'alarms': alarms
    }
