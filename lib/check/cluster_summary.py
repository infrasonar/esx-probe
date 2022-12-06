from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict
from ..vmwarequery import vmwarequery


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
    summary = {}
    hosts = {}

    for moref, cluster in clusters_lookup.items():
        cluster_name = f'{moref.parent.parent.name}-{moref.name}'

        dct = prop_val_to_dict(cluster['summary'], item_name=cluster_name)
        summary[cluster_name] = dct

        for host_moref in cluster['host']:
            host = hosts_lookup.get(host_moref)
            if host is None:
                continue

            cfg = prop_val_to_dict(host['summary'].config)
            host_dct = prop_val_to_dict(host['summary'])
            product_dct = prop_val_to_dict(host['summary'].config.product)
            host_dct['productName'] = product_dct['name']
            host_dct.update(cfg)
            host_dct.update(product_dct)
            host_dct['name'] = host['name']
            host_dct['clusterName'] = cluster_name
            hosts[host['name']] = host_dct

    return {
        'clusterSummary': summary,
        'hosts': hosts
    }
