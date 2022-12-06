from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery
from ..utils import datetime_to_timestamp


def on_about_info(obj):
    # vim.AboutInfo
    return {
        'name': 'product',
        'apiType': obj.apiType,  # str
        'apiVersion': obj.apiVersion,  # str
        'build': obj.build,  # str
        'fullName': obj.fullName,  # str
        'instanceUuid': obj.instanceUuid,  # str
        'licenseProductName': obj.licenseProductName,  # str
        'licenseProductVersion': obj.licenseProductVersion,  # str
        'localeBuild': obj.localeBuild,  # str
        'localeVersion': obj.localeVersion,  # str
        'name': obj.name,  # str
        'osType': obj.osType,  # str
        'productLineId': obj.productLineId,  # int
        'vendor': obj.vendor,  # str
        'version': obj.version,  # str
    }


def on_runtime_info(obj):
    # vim.host.Summary.RuntimeInfo
    return {
        'name': 'runtime',
        'bootTime': datetime_to_timestamp(obj.bootTime),  # int
        'connectionState': obj.connectionState,  # str
        'cryptoState': obj.cryptoState,  # str
        'hostMaxVirtualDiskCapacity': obj.hostMaxVirtualDiskCapacity,  # int
        'inMaintenanceMode': obj.inMaintenanceMode,  # bool
        'inQuarantineMode': obj.inQuarantineMode,  # bool/null
        'powerState': obj.powerState,  # str
        'standbyMode': obj.standbyMode,  # str/null
    }


def on_quick_stats(obj):
    # vim.host.Summary.QuickStats
    return {
        'name': 'quickStats',
        'availablePMemCapacity': obj.availablePMemCapacity,  # int/null
        'distributedCpuFairness': obj.distributedCpuFairness,  # int/null
        'distributedMemoryFairness': obj.distributedMemoryFairness,  # int/null
        'overallCpuUsage': obj.overallCpuUsage,  # int
        'overallMemoryUsage': obj.overallMemoryUsage,  # int
        'uptime': obj.uptime,  # int
    }


def on_hardware_summary(obj):
    # vim.host.Summary.HardwareSummary
    return {
        'name': 'hardware',
        'cpuMhz': obj.cpuMhz,  # int
        'cpuModel': obj.cpuModel,  # str
        'memorySize': obj.memorySize,  # int
        'model': obj.model,  # str
        'numCpuCores': obj.numCpuCores,  # int
        'numCpuPkgs': obj.numCpuPkgs,  # int
        'numCpuThreads': obj.numCpuThreads,  # int
        'numHBAs': obj.numHBAs,  # int
        'numNics': obj.numNics,  # int
        'uuid': obj.uuid,  # str
        'vendor': obj.vendor,  # str
    }


def on_config_summary(obj):
    # vim.host.Summary.ConfigSummary
    return {
        'name': obj.name,
        'faultToleranceEnabled': obj.faultToleranceEnabled,  # bool
        'port': obj.port,  # int
        'sslThumbprint': obj.sslThumbprint,  # int/null
        'vmotionEnabled': obj.vmotionEnabled,  # int
    }


def fmt_summary(summary) -> dict:
    output = {}
    output['quickStats'] = [on_quick_stats(summary.quickStats)]

    # TODO
    # output['hardwareOther'] = [
    #     {
    #         **{
    #             item.identifierType.key: item.identifierValue
    #             for item in summary.hardware.otherIdentifyingInfo
    #         },
    #         'name': 'hardwareOther',
    #     }
    # ]
    output['hardware'] = [on_hardware_summary(summary.hardware)]
    output['feature'] = [
        {
            'name': feature.key,
            'value': feature.value}
        for feature in summary.config.featureVersion
    ]
    output['product'] = [on_about_info(summary.config.product)]
    output['config'] = [on_config_summary(summary.config)]
    output['netstack'] = []
    output['nic'] = []
    net_runtime_info = summary.runtime.networkRuntimeInfo
    if net_runtime_info:
        for stackInfo in net_runtime_info.netStackInstanceRuntimeInfo:
            output['netstack'].append({
                'name': stackInfo.netStackInstanceKey,  # str
                'currentIpV6Enabled': stackInfo.currentIpV6Enabled,  # bool
                'maxNumberOfConnections':
                    stackInfo.maxNumberOfConnections,  # int
                'state': stackInfo.state,  # str
            })
            for nic in stackInfo.vmknicKeys:
                output['nic'].append({
                    'netstack': stackInfo.netStackInstanceKey,
                    'name': stackInfo.netStackInstanceKey + ':' + nic,
                    'nic': nic
                })
    output['runtime'] = [on_runtime_info(summary.runtime)]
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
