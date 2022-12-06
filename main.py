from libprobe.probe import Probe
from lib.check.vmware import check_vmware
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'vmware': check_vmware
    }

    probe = Probe("vmware", version, checks)

    probe.start()
