import logging
import time
from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import datetime_to_timestamp
from ..utils import on_host_summary
from ..utils import on_config_summary
from ..utils import on_about_info
from ..vmwarequery import vmwarequery


def on_guest_info(obj):
    # vim.vm.GuestInfo
    return {
        'appHeartbeatStatus': obj.appHeartbeatStatus,  # str
        'appState': obj.appState,  # str
        'guestFamily': obj.guestFamily,  # str
        'guestFullName': obj.guestFullName,  # str
        'guestId': obj.guestId,  # str
        'guestKernelCrashed': obj.guestKernelCrashed,  # bool
        'guestOperationsReady': obj.guestOperationsReady,  # bool
        'guestState': obj.guestState,  # str
        'guestStateChangeSupported': obj.guestStateChangeSupported,  # bool
        'hostName': obj.hostName,  # str
        'hwVersion': obj.hwVersion,  # str
        'interactiveGuestOperationsReady':
            obj.interactiveGuestOperationsReady,  # bool
        'ipAddress': obj.ipAddress,  # str
        'toolsInstallType': obj.toolsInstallType,  # str
        'toolsRunningStatus': obj.toolsRunningStatus,  # str
        'toolsStatus': obj.toolsStatus,  # str
        'toolsVersion': obj.toolsVersion,  # str
        'toolsVersionStatus': obj.toolsVersionStatus,  # str
        'toolsVersionStatus2': obj.toolsVersionStatus2,  # str
    }


def on_runtime_info(obj):
    # vim.vm.RuntimeInfo
    return {
        'bootTime': datetime_to_timestamp(obj.bootTime),
        'cleanPowerOff': obj.cleanPowerOff,  # bool
        'connectionState': obj.connectionState,  # str
        'consolidationNeeded': obj.consolidationNeeded,  # str
        'cryptoState': obj.cryptoState,  # str/null
        'dasVmProtection': obj.dasVmProtection,  # str/null
        'faultToleranceState': obj.faultToleranceState,  # str
        'instantCloneFrozen': obj.instantCloneFrozen,  # bool
        'maxCpuUsage': obj.maxCpuUsage,  # int
        'maxMemoryUsage': obj.maxMemoryUsage,  # int
        'memoryOverhead': obj.memoryOverhead,  # int
        'minRequiredEVCModeKey': obj.minRequiredEVCModeKey,  # str
        'needSecondaryReason': obj.needSecondaryReason,  # str/null
        'numMksConnections': obj.numMksConnections,  # int
        'onlineStandby': obj.onlineStandby,  # bool
        'paused': obj.paused,  # bool
        'powerState': obj.powerState,  # str
        'question': obj.question,  # str/null
        'quiescedForkParent': obj.quiescedForkParent,  # bool/null
        'recordReplayState': obj.recordReplayState,  # str
        'snapshotInBackground': obj.snapshotInBackground,  # bool
        'suspendInterval': obj.suspendInterval,  # int
        'suspendTime': datetime_to_timestamp(obj.suspendTime),
        'suspendedToMemory': obj.suspendedToMemory,  # bool
        'toolsInstallerMounted': obj.toolsInstallerMounted,  # bool
        'vFlashCacheAllocation': obj.vFlashCacheAllocation,  # int
        'vmFailoverInProgress': obj.vmFailoverInProgress,  # int
    }


def on_virtual_hardware(obj):
    # vim.vm.VirtualHardware
    return {
        'memoryMB': obj.memoryMB,
        'numCPU': obj.numCPU,
        'numCoresPerSocket': obj.numCoresPerSocket,
        'virtualICH7MPresent': obj.virtualICH7MPresent,
        'virtualSMCPresent': obj.virtualSMCPresent,
    }


def on_config_info(obj):
    # vim.vm.ConfigSpec
    return {
        **on_virtual_hardware(obj.hardware),
        'alternateGuestName': obj.alternateGuestName,  # str
        'annotation': obj.annotation,  # str
        'changeTrackingEnabled': obj.changeTrackingEnabled,  # bool
        'changeVersion': obj.changeVersion,  # str
        'createDate': datetime_to_timestamp(obj.createDate),
        'cpuHotAddEnabled': obj.cpuHotAddEnabled,  # bool
        'cpuHotRemoveEnabled': obj.cpuHotRemoveEnabled,  # bool
        'firmware': obj.firmware,  # str
        'ftEncryptionMode': obj.ftEncryptionMode,  # str
        'guestAutoLockEnabled': obj.guestAutoLockEnabled,  # bool
        'guestFullName': obj.guestFullName,  # str
        'guestId': obj.guestId,  # str
        'hotPlugMemoryIncrementSize': obj.hotPlugMemoryIncrementSize,  # str
        'hotPlugMemoryLimit': obj.hotPlugMemoryLimit,  # str
        'instanceUuid': obj.instanceUuid,  # str
        'locationId': obj.locationId,  # str
        'maxMksConnections': obj.maxMksConnections,  # int
        'memoryHotAddEnabled': obj.memoryHotAddEnabled,  # bool
        'memoryReservationLockedToMax':
            obj.memoryReservationLockedToMax,  # bool
        'messageBusTunnelEnabled': obj.messageBusTunnelEnabled,  # bool
        'migrateEncryption': obj.migrateEncryption,  # str
        'modified': datetime_to_timestamp(obj.modified),
        'name': obj.name,  # str
        'nestedHVEnabled': obj.nestedHVEnabled,  # bool
        'npivDesiredNodeWwns': obj.npivDesiredNodeWwns,  # int/null
        'npivDesiredPortWwns': obj.npivDesiredPortWwns,  # int/null
        'migrateEncryption': obj.migrateEncryption,  # str
        # 'npivNodeWorldWideName': obj.npivNodeWorldWideName,  # [int]
        'npivOnNonRdmDisks': obj.npivOnNonRdmDisks,  # bool
        # 'npivPortWorldWideName': obj.npivPortWorldWideName,  # [int]
        'npivTemporaryDisabled': obj.npivTemporaryDisabled,  # bool
        'npivWorldWideNameType': obj.npivWorldWideNameType,  # str
        'pmemFailoverEnabled': obj.pmemFailoverEnabled,  # str
        'sevEnabled': obj.sevEnabled,  # bool
        'swapPlacement': obj.swapPlacement,  # str
        'swapStorageObjectId': obj.swapStorageObjectId,  # str
        'template': obj.template,  # bool
        'uuid': obj.uuid,  # str
        'vAssertsEnabled': obj.vAssertsEnabled,  # bool
        'vFlashCacheReservation': obj.vFlashCacheReservation,  # int
        'vPMCEnabled': obj.vPMCEnabled,  # bool
        'version': obj.version,  # str
        'vmOpNotificationToAppEnabled':
            obj.vmOpNotificationToAppEnabled,  # int
        'vmStorageObjectId': obj.vmStorageObjectId,  # str
        'vmxConfigChecksum': obj.vmxConfigChecksum,  # str/null
    }


def on_virtual_disk_backing_info(obj):
    # vim.vm.device.VirtualDisk.FlatVer2BackingInfo
    return {
        'changeId': obj.changeId,  # str/null
        'contentId': obj.contentId,  # str
        'deltaDiskFormat': obj.deltaDiskFormat,  # str
        'deltaDiskFormatVariant': obj.deltaDiskFormatVariant,  # str
        'deltaGrainSize': obj.deltaGrainSize,  # int
        'digestEnabled': obj.digestEnabled,  # bool
        'diskMode': obj.diskMode,  # str
        'eagerlyScrub': obj.eagerlyScrub,  # bool
        'fileName': obj.fileName,  # str
        'sharing': obj.sharing,  # str
        'split': obj.split,  # bool
        'thinProvisioned': obj.thinProvisioned,  # bool
        'uuid': obj.uuid,  # str
        'writeThrough': obj.writeThrough,  # bool
    }


def on_virtual_disk(obj):
    # vim.vm.device.VirtualDisk
    return {
        **on_virtual_disk_backing_info(obj.backing),
        'capacityInBytes': obj.capacityInBytes,  # int
        'capacityInKB': obj.capacityInKB,  # int/null
        'diskObjectId': obj.diskObjectId,  # str/null
        'nativeUnmanagedLinkedClone': obj.nativeUnmanagedLinkedClone,  # bool
    }


def on_snapshot_tree(obj):
    # vim.vm.SnapshotTree
    return {
        'backupManifest': obj.backupManifest,  # str
        'createTime': datetime_to_timestamp(obj.createTime),
        'description': obj.description,  # str
        'id': obj.id,  # int
        # 'name': obj.name,  # str
        'quiesced': obj.quiesced,  # xsd:boolean
        'replaySupported': obj.replaySupported,  # xsd:boolean
        'state': obj.state,  # str
    }


def snapshot_flat(snapshots, vm_name, current_time):
    for snapshot in snapshots:
        snapshot_dct = on_snapshot_tree(snapshot)
        snapshot_dct['name'] = str(snapshot.id)
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
        if 'config' not in vm:
            logging.info(
                f'Skipping VM {vm} because it is missing config data'
            )
            continue
        if vm['config'].template:
            continue
        lookup_info = {'sourceProbeName': 'vmwareProbe'}
        fqdn = vm['guest'].hostName
        if vm['guest'].ipAddress:
            lookup_info['ip4'] = vm['guest'].ipAddress
        lookup_info['name'] = vm['name']
        lookup_info['moref'] = moref._moId
        lookup_info['sourceUniqueId'] = instance_uuid = \
            vm['config'].instanceUuid
        vm['lookupInfo'] = lookup_info

        # CHECK HOST VMS
        info_dct = on_guest_info(vm['guest'])
        info_dct['name'] = instance_uuid
        info_dct['instanceName'] = vm['name']
        guests.append(info_dct)

        # INFO
        vm['instanceUuid'] = instance_uuid

        # SNAPSHOTS
        if 'snapshot' in vm:
            snap_lst = list(
                snapshot_flat(
                    vm['snapshot'].rootSnapshotList,
                    vm['name'],
                    ts))

            for snap_dct in snap_lst:
                snapshots.append(snap_dct)

        for device in vm['config'].hardware.device:
            if (device.key >= 2000) and (device.key < 3000):
                # DISKS
                disk_dct = on_virtual_disk(device)
                disk_dct['name'] = device.backing.fileName

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
            runtime_dct = on_runtime_info(vm['runtime'])
            runtime_dct['name'] = instance_uuid
            runtime_dct['fqdn'] = fqdn
            runtimes.append(runtime_dct)

            moref = vm['runtime'].host
            hyp = hypervisors_lookup.get(moref)
            if hyp:
                host_dct = {
                    **on_host_summary(hyp['summary']),
                    **on_config_summary(hyp['summary'].config),
                    **on_about_info(hyp['summary'].config.product),
                    'productName': hyp['summary'].config.product.name,
                    'name': hyp['name'],
                }
                hypervisors.append(host_dct)

                runtime_dct['currentHypervisor'] = hyp['name']
                info_dct['currentHypervisor'] = hyp['name']

        # CONFIG
        cfg_dct = on_config_info(vm['config'])
        cfg_dct['name'] = instance_uuid
        cfg_dct['fqdn'] = fqdn
        guest_configs.append(cfg_dct)

    guest_count = [{
        'name': 'guestCount',
        'guestCount': len(guests),
        'runningGuestCount': sum(
            guest.get('guestState') == 'running'
            for guest in guests)
    }]

    return {
        'guests': guests,
        'guestConfigs': guest_configs,
        'guestCount': guest_count,
        'hypervisors': hypervisors,
        'virtualDisks': virtual_disks,
        'snapShots': snapshots,
        'runtimes': runtimes,
        'virtualStorage': list(virtual_storage_capacities.values())
    }
