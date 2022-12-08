from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


def fmt_issue(issue) -> dict:
    # vim.event.EventEx

    severity = getattr(issue.severity, None)  # str/null
    if severity is None:
        # see vim.event.EventEx docs
        severity = 'info'

    return {
        'name': str(issue.key),  # int
        'severity': severity,
        'eventTypeId': issue.eventTypeId,  # str
        'fullFormattedMessage': issue.fullFormattedMessage,  # str
    }


async def check_config_issues(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
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
        'configIssue': issues
    }
