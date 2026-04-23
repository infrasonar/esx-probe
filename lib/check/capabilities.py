from libprobe.asset import Asset
from libprobe.check import Check
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


class CheckCapabilities(Check):
    key = 'capabilities'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        result = await vmwarequery(
            asset,
            local_config,
            config,
            vim.HostSystem,
            ['capability'],
        )

        capabilities = [
            {
                'name': name,
                'capability': getattr(prop.val, name)
            }
            for item in result
            for prop in item.propSet
            for name in prop.val._propInfo
            if isinstance(getattr(prop.val, name, None), bool)
        ]

        return {
            'capability': capabilities
        }
