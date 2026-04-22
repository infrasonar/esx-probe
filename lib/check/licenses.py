from libprobe.asset import Asset
from libprobe.check import Check
from pyVmomi import vim
from ..vmwarequery import vmwarequery


class CheckLicenses(Check):
    key = 'licenses'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        result = await vmwarequery(
            asset,
            local_config,
            config,
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
            'licenses': licenses
        }
