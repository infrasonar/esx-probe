from libprobe.asset import Asset
from libprobe.check import Check
from pyVmomi import vim
from ..vmwarequery import vmwarequery


def fmt_issue(issue) -> dict:
    # vim.event.EventEx

    severity = getattr(issue, 'severity', None)  # str/null
    if severity is None:
        # see vim.event.EventEx docs
        severity = 'info'

    return {
        'name': str(issue.key),  # int
        'severity': severity,
        'eventTypeId': issue.eventTypeId,  # str
        'fullFormattedMessage': issue.fullFormattedMessage,  # str
    }


class CheckConfigIssues(Check):
    key = 'configIssues'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        result = await vmwarequery(
            asset,
            local_config,
            config,
            vim.HostSystem,
            ['configIssue'],
        )

        issues = [
            fmt_issue(issue)
            for item in result
            for prop in item.propSet
            for issue in prop.val
            if isinstance(issue, vim.event.EventEx)
        ]

        return {
            'configIssues': issues
        }
