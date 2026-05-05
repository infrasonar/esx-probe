from libprobe.asset import Asset
from libprobe.check import Check
from pyVmomi import vim
from ..vmwarequery import vmwarequery


class CheckNetwork(Check):
    key = 'network'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        result = await vmwarequery(
            asset,
            local_config,
            config,
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
