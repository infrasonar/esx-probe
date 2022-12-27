import logging
from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import datetime_to_timestamp
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
        'bootTime': datetime_to_timestamp(obj.bootTime),  # int/null
        'cleanPowerOff': obj.cleanPowerOff,  # bool
        'connectionState': obj.connectionState,  # str
        'consolidationNeeded': obj.consolidationNeeded,  # str
        'cryptoState': obj.cryptoState,  # str/null
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
        'quiescedForkParent': obj.quiescedForkParent,  # bool/null
        'recordReplayState': obj.recordReplayState,  # str
        'snapshotInBackground': obj.snapshotInBackground,  # bool
        'suspendInterval': obj.suspendInterval,  # int
        'suspendTime': datetime_to_timestamp(obj.suspendTime),
        'toolsInstallerMounted': obj.toolsInstallerMounted,  # bool
        'vFlashCacheAllocation': obj.vFlashCacheAllocation,  # int
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
    # vim.vm.ConfigInfo
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
        'guestAutoLockEnabled': obj.guestAutoLockEnabled,  # bool
        'guestFullNameConfig': obj.guestFullName,  # str
        'guestIdConfig': obj.guestId,  # str
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
        # 'name': obj.name,  # str
        'nestedHVEnabled': obj.nestedHVEnabled,  # bool
        'npivDesiredNodeWwns': obj.npivDesiredNodeWwns,  # int/null
        'npivDesiredPortWwns': obj.npivDesiredPortWwns,  # int/null
        'migrateEncryption': obj.migrateEncryption,  # str
        'npivOnNonRdmDisks': obj.npivOnNonRdmDisks,  # bool
        'npivTemporaryDisabled': obj.npivTemporaryDisabled,  # bool
        'npivWorldWideNameType': obj.npivWorldWideNameType,  # str
        'swapPlacement': obj.swapPlacement,  # str
        'swapStorageObjectId': obj.swapStorageObjectId,  # str
        'template': obj.template,  # bool
        'uuid': obj.uuid,  # str
        'vAssertsEnabled': obj.vAssertsEnabled,  # bool
        'vFlashCacheReservation': obj.vFlashCacheReservation,  # int
        'vPMCEnabled': obj.vPMCEnabled,  # bool
        'version': obj.version,  # str
        'vmStorageObjectId': obj.vmStorageObjectId,  # str
    }


def on_virtual_disk_backing_info(obj):
    # vim.vm.device.VirtualDisk.FlatVer2BackingInfo
    return {
        'changeId': obj.changeId,  # str/null
        'contentId': obj.contentId,  # str/null
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
        'diskObjectId': obj.diskObjectId,  # str/null
        'nativeUnmanagedLinkedClone':
            obj.nativeUnmanagedLinkedClone,  # bool/null
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


def snapshot_flat(snapshots, vm_name):
    for snapshot in snapshots:
        snapshot_dct = on_snapshot_tree(snapshot)
        snapshot_dct['name'] = str(snapshot.id)
        snapshot_dct['snapshotName'] = snapshot.name
        snapshot_dct['snapshotId'] = snapshot.id
        snapshot_dct['vm'] = vm_name
        yield snapshot_dct
        for item in snapshot_flat(
                snapshot.childSnapshotList, vm_name):
            item['parentSnapshotName'] = snapshot.name
            item['parentSnapshotId'] = snapshot.id
            yield item


async def check_host_vms(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    stores_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.Datastore,
        ['name', 'summary.capacity', 'info'],
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
    vms_retrieved = {
        vm.obj: {p.name: p.val for p in vm.propSet} for vm in vms_}

    guests = []
    virtual_disks = []
    snapshots = []
    virtual_storage_capacities = {}

    for moref, vm in vms_retrieved.items():
        if 'config' not in vm:
            logging.info(
                f'Skipping VM {vm} because it is missing config data'
            )
            continue
        if vm['config'].template:
            continue

        # CHECK HOST VMS
        info_dct = on_guest_info(vm['guest'])
        info_dct.update(on_config_info(vm['config']))
        info_dct.update(on_runtime_info(vm['runtime']))
        info_dct['name'] = vm['config'].instanceUuid
        info_dct['instanceName'] = vm['name']
        guests.append(info_dct)

        # SNAPSHOTS
        if 'snapshot' in vm:
            snapshots.extend(
                snapshot_flat(
                    vm['snapshot'].rootSnapshotList, vm['name']))

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

    guest_count = [{
        'name': 'guestCount',
        'guestCount': len(guests),
        'runningGuestCount': sum(
            guest.get('guestState') == 'running'
            for guest in guests)
    }]

    return {
        'guests': guests,
        'guestCount': guest_count,
        'virtualDisks': virtual_disks,
        'snapshots': snapshots,
        'virtualStorage': list(virtual_storage_capacities.values())
    }
