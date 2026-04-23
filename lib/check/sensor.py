from libprobe.asset import Asset
from libprobe.check import Check
from pyVmomi import vim
from ..vmwarequery import vmwarequery


class CheckSensor(Check):
    key = 'sensor'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        result = await vmwarequery(
            asset,
            local_config,
            config,
            vim.HostSystem,
            ['runtime.healthSystemRuntime.systemHealthInfo.numericSensorInfo'],
        )

        sensors = [
            # vim.host.NumericSensorInfo
            {
                'name': prop_val.name,  # str
                'healthState': prop_val.healthState.key,  # str
                'readingValue': prop_val.currentReading * float(
                    10 ** prop_val.unitModifier),
                'baseUnits': prop_val.baseUnits,  # str
                'currentReading': prop_val.currentReading,  # int
                'rateUnits': prop_val.rateUnits,  # str
                'sensorType': prop_val.sensorType,  # str
                'unitModifier': prop_val.unitModifier,  # int
            }
            for item in result
            for prop in item.propSet
            for prop_val in prop.val
        ]

        return {
            'sensor': sensors
        }
