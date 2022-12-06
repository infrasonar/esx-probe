import logging
import time
from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import prop_val_to_dict, hostname_to_valid_fqdn
from ..vmwarequery import vmwarequery


def snapshot_flat(snapshots, vm_name, current_time):
    for snapshot in snapshots:
        snapshot_dct = \
            prop_val_to_dict(snapshot, item_name=snapshot.id)
        snapshot_dct['snapshotName'] = snapshot.name
        snapshot_dct['snapshotId'] = snapshot.id
        snapshot_dct['vm'] = vm_name
        create_time = snapshot_dct.get('createTime')
        if create_time:
            snapshot_dct['age'] = current_time - create_time
        yield snapshot_dct
        for item in snapshot_flat(
                snapshot.childSnapshotList, vm_name, current_time):
            item['parentSnapShotId'] = snapshot.id
            item['parentSnapShotName'] = snapshot.name
            yield item


async def check_host_vms(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    ts = int(time.time())

    stores_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.Datastore,
        ['name', 'summary.capacity', 'info'],
    )

    hypervisors_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['name', 'summary'],
    )

    vms_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.VirtualMachine,
        ['name', 'config', 'guest', 'snapshot', 'runtime'],
    )

    stores_lookup = {
        store.obj: {p.name: p.val for p in store.propSet} for store in stores_}
    hypervisors_lookup = {
        hyp.obj: {p.name: p.val for p in hyp.propSet} for hyp in hypervisors_}
    vms_retrieved = {
        vm.obj: {p.name: p.val for p in vm.propSet} for vm in vms_}

    guests = []
    virtual_disks = []
    snapshots = []
    virtual_storage_capacities = {}
    runtimes = []
    hypervisors = []
    guest_configs = []

    for moref, vm in vms_retrieved.items():
        try:
            if 'config' not in vm:
                logging.info(
                    f'Skipping VM {vm} because it is missing config data'
                )
                continue
            if vm['config'].template:
                continue
            lookup_info = {'sourceProbeName': 'vmwareProbe'}
            guest_check = {
                'config': {},
                'info': {},
                'networks': {},
                'snapshots': {},
                'datastores': {},
                'routes': {},
                'dns': {},
                'nics': {},
                'disks': {},
                'runtime': {}
            }

            fqdn = vm['guest'].hostName

            for ip_stack in vm['guest'].ipStack:

                if ip_stack.dnsConfig:
                    # DNS
                    dns = prop_val_to_dict(ip_stack.dnsConfig)
                    stack_fqdn = dns['hostName']
                    stack_domain = dns.get('domainName')
                    if stack_domain and stack_fqdn:
                        stack_fqdn += '.' + stack_domain
                        if fqdn is None:
                            fqdn = stack_fqdn
                        elif '.' not in fqdn and '.' in stack_fqdn:
                            fqdn = stack_fqdn
                    if stack_fqdn:
                        stack_fqdn = stack_fqdn.lower()
                        dns['name'] = stack_fqdn
                        guest_check['dns'][stack_fqdn] = dns
                        for idx, ip in enumerate(
                                ip_stack.dnsConfig.ipAddress):
                            dns['dnsIp{}'.format(idx + 1)] = ip

            if vm['guest'].ipAddress:
                lookup_info['ip4'] = vm['guest'].ipAddress
            lookup_info['name'] = vm['name']
            lookup_info['moref'] = moref._moId
            lookup_info['sourceUniqueId'] = instance_uuid = \
                vm['config'].instanceUuid
            vm['lookupInfo'] = lookup_info

            if not fqdn:
                fqdn = hostname_to_valid_fqdn(vm['name'])
            fqdn = fqdn.lower()

            # CHECK HOST VMS
            info_dct = prop_val_to_dict(
                vm['guest'], item_name=instance_uuid)
            info_dct['instanceName'] = vm['name']
            info_dct['fqnd'] = fqdn
            guests.append(info_dct)
            guest_check['info'] = {instance_uuid: info_dct}
            # INFO

            vm['fqdn'] = fqdn
            vm['instanceUuid'] = instance_uuid

            # SNAPSHOTS
            if 'snapshot' in vm:
                snap_lst = list(
                    snapshot_flat(
                        vm['snapshot'].rootSnapshotList,
                        vm['name'],
                        ts))

                for snap_dct in snap_lst:
                    guest_check['snapshots'][snap_dct['name']] = snap_dct
                    snapshots.append(snap_dct)

            for device in vm['config'].hardware.device:
                if (device.key >= 2000) and (device.key < 3000):
                    # DISKS
                    disk_dct = prop_val_to_dict(
                        device, item_name=device.backing.fileName)
                    disk_dct.update(prop_val_to_dict(device.backing))
                    disk_dct['fileName'] = \
                        getattr(device.backing, 'fileName', None)
                    datastore = stores_lookup[device.backing.datastore]
                    datastore_name = datastore['name']
                    disk_dct['datastore'] = datastore['name']
                    if hasattr(device, 'deviceInfo') and device.deviceInfo:
                        disk_dct['label'] = device.deviceInfo.label
                    if disk_dct['capacityInBytes'] and \
                            disk_dct['datastore']:
                        if datastore_name not in \
                                virtual_storage_capacities:
                            virtual_storage_capacities[datastore_name] = {
                                'virtualCapacity': 0,
                                'name': datastore_name,
                                'actualCapacity': datastore[
                                    'summary.capacity']}
                        virtual_storage_capacities[datastore_name][
                            'virtualCapacity'] += disk_dct[
                                'capacityInBytes']
                    virtual_disks.append(disk_dct)

            if 'runtime' in vm and vm['runtime']:
                runtime_dct = disk_dct = prop_val_to_dict(
                    vm['runtime'], item_name=instance_uuid)
                runtime_dct['fqdn'] = fqdn
                guest_check['runtime'][instance_uuid] = runtime_dct
                runtimes.append(runtime_dct)

                moref = vm['runtime'].host
                hyp = hypervisors_lookup.get(moref)
                if hyp:
                    cfg = prop_val_to_dict(hyp['summary'].config)
                    host_dct = prop_val_to_dict(hyp['summary'])
                    product_dct = prop_val_to_dict(
                        hyp['summary'].config.product)
                    host_dct['productName'] = product_dct['name']
                    host_dct.update(cfg)
                    host_dct.update(product_dct)
                    host_dct['name'] = hyp['name']
                    hypervisors.append(host_dct)

                    runtime_dct['currentHypervisor'] = hyp['name']
                    info_dct['currentHypervisor'] = hyp['name']

            # CONFIG
            cfg_dct = prop_val_to_dict(
                vm['config'], item_name=instance_uuid)
            cfg_dct.update(prop_val_to_dict(vm['config'].hardware))
            cfg_dct['fqdn'] = fqdn
            guest_check['config'] = {instance_uuid: cfg_dct}
            guest_configs.append(cfg_dct)
        except Exception:
            logging.exception('')

    guest_count = {'name': 'guestCount', 'guestCount': len(guests),
                   'runningGuestCount': sum(
        1 for guest in guests
        if guest.get('guestState') == 'running')}

    # TODO waarom is dit < 0?
    for ds in virtual_storage_capacities.values():
        try:
            ds['overProvisionPerc'] = (
                100.0 * ds['virtualCapacity'] / ds['actualCapacity']
            ) - 100.0
        except Exception:
            pass

    return {
        'guests': guests,
        'guestConfigs': guest_configs,
        'guestCount': [guest_count],
        'hypervisors': hypervisors,
        'virtualDisks': virtual_disks,
        'snapShots': snapshots,
        'runtimes': runtimes,
        'virtualStorage': list(virtual_storage_capacities.values())
    }
