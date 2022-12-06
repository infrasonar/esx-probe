from libprobe.probe import Probe
from lib.check.alarms import check_alarms
from lib.check.capabilities import check_capabilities
from lib.check.config_issues import check_config_issues
from lib.check.cluster_summary import check_cluster_summary
from lib.check.cpu_pkg import check_cpu_pkg
from lib.check.datastore_summary import check_datastore_summary
from lib.check.hardware_status import check_hardware_status
from lib.check.host_summary import check_host_summary
from lib.check.host_vms import check_host_vms
from lib.check.licenses import check_licenses
from lib.check.network_summary import check_network_summary
from lib.check.pci import check_pci
from lib.check.sensor_info import check_sensor_info
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'alarms': check_alarms,
        'capabilities': check_capabilities,
        'clusterSummary': check_cluster_summary,
        'configIssues': check_config_issues,
        'cpuPkg': check_cpu_pkg,
        'datastoreSummary': check_datastore_summary,
        'hardwareStatus': check_hardware_status,
        'hostSummary': check_host_summary,
        'hostVMs': check_host_vms,
        'licences': check_licenses,
        'networkSummary': check_network_summary,
        'pci': check_pci,
        'sensorInfo': check_sensor_info,
    }

    probe = Probe("vmware", version, checks)

    probe.start()
