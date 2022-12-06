from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


def on_about_info(obj):
    # vim.AboutInfo
    return {
        'apiType': obj.apiType,  # str
        'apiVersion': obj.apiVersion,  # str
        'build': obj.build,  # str
        'fullName': obj.fullName,  # str
        'instanceUuid': obj.instanceUuid,  # str
        'licenseProductName': obj.licenseProductName,  # str
        'licenseProductVersion': obj.licenseProductVersion,  # str
        'localeBuild': obj.localeBuild,  # str
        'localeVersion': obj.localeVersion,  # str
        'osType': obj.osType,  # str
        'productLineId': obj.productLineId,  # int
        'productName': obj.name,  # str
        'vendor': obj.vendor,  # str
        'version': obj.version,  # str
    }


def on_config_summary(obj):
    # vim.host.Summary.ConfigSummary
    return {
        **on_about_info(obj.product),
        'faultToleranceEnabled': obj.faultToleranceEnabled,  # bool
        'port': obj.port,  # int
        'sslThumbprint': obj.sslThumbprint,  # int
        'vmotionEnabled': obj.vmotionEnabled,  # int
    }


def on_host_summary(obj):
    # vim.host.Summary
    return {
        **on_config_summary(obj.config),
        'currentEVCModeKey': obj.currentEVCModeKey,  # str
        'managementServerIp': obj.managementServerIp,  # str
        'maxEVCModeKey': obj.maxEVCModeKey,  # str
        'overallStatus': obj.overallStatus,  # str
        'rebootRequired': obj.rebootRequired,  # bool
    }


def on_cluster_summary(obj):
    # vim.ClusterComputeResource.Summary
    return {
        'currentBalance': obj.currentBalance,  # int
        'currentEVCModeKey': obj.currentEVCModeKey,  # str
        'currentFailoverLevel': obj.currentFailoverLevel,  # int
        'numVmotions': obj.numVmotions,  # int
        'targetBalance': obj.targetBalance,  # int
    }


async def check_cluster_summary(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    hosts_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['name', 'summary'],
    )
    clusters_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.ClusterComputeResource,
        ['summary', 'host'],
    )

    clusters_lookup = {
        c.obj: {p.name: p.val for p in c.propSet} for c in clusters_}
    hosts_lookup = {
        h.obj: {p.name: p.val for p in h.propSet} for h in hosts_}
    summary = []
    hosts = {}

    for moref, cluster in clusters_lookup.items():
        cluster_name = f'{moref.parent.parent.name}-{moref.name}'
        cluster_dct = on_cluster_summary(cluster['summary'])
        cluster_dct['name'] = cluster_name
        summary.append(cluster_dct)

        for host_moref in cluster['host']:
            host = hosts_lookup.get(host_moref)
            if host is None:
                continue

            host_dct = on_host_summary(host['summary'])
            host_dct['name'] = host['name']
            host_dct['clusterName'] = cluster_name
            hosts.append(host_dct)

    return {
        'clusterSummary': summary,
        'hosts': hosts
    }
