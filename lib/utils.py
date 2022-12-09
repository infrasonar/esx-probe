import calendar


def datetime_to_timestamp(inp):
    if inp is None:
        return inp
    return calendar.timegm(inp.timetuple())


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
        'name': obj.name,  # str
        'osType': obj.osType,  # str
        'patchLevel': obj.patchLevel,  # str
        'productLineId': obj.productLineId,  # int
        'vendor': obj.vendor,  # str
        'version': obj.version,  # str
    }


def on_config_summary(obj):
    # vim.host.Summary.ConfigSummary
    return {
        'faultToleranceEnabled': obj.faultToleranceEnabled,  # bool
        'name': obj.name,  # str
        'port': obj.port,  # int
        'sslThumbprint': obj.sslThumbprint,  # int/null
        'vmotionEnabled': obj.vmotionEnabled,  # int
    }


def on_host_summary(obj):
    # vim.host.Summary
    return {
        'currentEVCGraphicsModeKey': obj.currentEVCGraphicsModeKey,  # str
        'currentEVCModeKey': obj.currentEVCModeKey,  # str
        'managementServerIp': obj.managementServerIp,  # str
        'maxEVCModeKey': obj.maxEVCModeKey,  # str
        'overallStatus': obj.overallStatus,  # str
        'rebootRequired': obj.rebootRequired,  # bool
    }
