from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict, datetime_to_timestamp
from ..vmwarequery import vmwarequery


# TODO andere itemnaam functie?
def fmt_issue(issue) -> dict:
    dct = prop_val_to_dict(issue)
    dct['name'] = str(datetime_to_timestamp(issue.createdTime)
                      ) + str(hash(dct.get('fullFormattedMessage')))
    return dct


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
    ]

    return {
        'configIssue': issues
    }
