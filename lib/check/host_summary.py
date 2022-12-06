from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery
from ..utils import prop_val_to_dict
from ..utils import dyn_property_list_to_dict
from ..utils import dyn_property_list_to_kv_list


def fmt_summary(summary) -> dict:
    output = {}
    output['quickStats'] = [
        prop_val_to_dict(
            summary.quickStats,
            item_name='quickStats')]
    output['hardwareOther'] = [
        dyn_property_list_to_dict(
            summary.hardware.otherIdentifyingInfo,
            item_name='hardwareOther')]
    output['hardware'] = [
        prop_val_to_dict(
            summary.hardware,
            item_name='hardware')]
    output['feature'] = dyn_property_list_to_kv_list(
        summary.config.featureVersion)
    output['product'] = [
        prop_val_to_dict(
            summary.config.product,
            item_name='product')]
    output['config'] = [prop_val_to_dict(summary.config)]
    output['netstack'] = []
    output['nic'] = []
    net_runtime_info = summary.runtime.networkRuntimeInfo
    if net_runtime_info:
        for stackInfo in net_runtime_info.netStackInstanceRuntimeInfo:
            output['netstack'].append(
                prop_val_to_dict(
                    stackInfo, item_name='netstack'))
            for nic in stackInfo.vmknicKeys:
                output['nic'].append({
                    'netstack': stackInfo.netStackInstanceKey,
                    'name': stackInfo.netStackInstanceKey + ':' + nic,
                    'nic': nic
                })
    output['runtime'] = [
        prop_val_to_dict(
            summary.runtime,
            item_name='runtime')]
    return output


async def check_host_summary(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['summary']
    )

    return {
        tp_name: tp
        for item in result
        for prop in item.propSet
        for tp_name, tp in fmt_summary(prop.val).items()
    }
