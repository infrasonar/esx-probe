from libprobe.probe import Probe
from lib.check.alarms import CheckAlarms
from lib.check.capabilities import CheckCapabilities
from lib.check.config_issues import CheckConfigIssues
from lib.check.datastore import CheckDatastore
from lib.check.hardware_status import CheckHardwareStatus
from lib.check.host import CheckHost
from lib.check.host_vms import CheckHostVMs
from lib.check.licenses import CheckLicenses
from lib.check.network import CheckNetwork
from lib.check.sensor import CheckSensor
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckAlarms,
        CheckCapabilities,
        CheckConfigIssues,
        CheckDatastore,
        CheckHardwareStatus,
        CheckHost,
        CheckHostVMs,
        CheckLicenses,
        CheckNetwork,
        CheckSensor,
    )

    probe = Probe("esx", version, checks)

    probe.start()
