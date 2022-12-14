from libprobe.probe import Probe
from lib.check.alarms import check_alarms
from lib.check.capabilities import check_capabilities
from lib.check.config_issues import check_config_issues
from lib.check.datastore import check_datastore
from lib.check.hardware_status import check_hardware_status
from lib.check.host import check_host
from lib.check.host_vms import check_host_vms
from lib.check.licenses import check_licenses
from lib.check.network import check_network
from lib.check.sensor import check_sensor
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'alarms': check_alarms,
        'capabilities': check_capabilities,
        'configIssues': check_config_issues,
        'datastore': check_datastore,
        'hardwareStatus': check_hardware_status,
        'host': check_host,
        'hostVMs': check_host_vms,
        'licences': check_licenses,
        'network': check_network,
        'sensor': check_sensor,
    }

    probe = Probe("esx", version, checks)

    probe.start()
