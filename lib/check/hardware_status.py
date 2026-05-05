from itertools import chain
from libprobe.asset import Asset
from libprobe.check import Check
from pyVmomi import vim
from ..vmwarequery import vmwarequery


class CheckHardwareStatus(Check):
    key = 'hardwareStatus'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        result = await vmwarequery(
            asset,
            local_config,
            config,
            vim.HostSystem,
            ['runtime.healthSystemRuntime.hardwareStatusInfo'],
        )

        hardware_status = [
            {
                'name': si.name,
                'status': si.status.key,
            }
            for item in result
            for prop in item.propSet
            for si in chain(
                prop.val.memoryStatusInfo,
                prop.val.cpuStatusInfo,
                prop.val.storageStatusInfo,
            )
        ]

        return {
            'hardwareStatus': hardware_status
        }
