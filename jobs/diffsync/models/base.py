import ipaddress

from diffsync import DiffSyncModel
from typing import List, Optional

from nautobot_ssot.contrib import NautobotModel
from nautobot.virtualization.models import (
    VirtualMachine as OrmVirtualMachine,
    VMInterface as OrmVMInterface,
)
from nautobot.ipam.models import (
    IPAddress as OrmIPAddress,
    IPAddressToInterface as OrmIPAddressToInterface,
    Prefix as OrmPrefix,
)
from nautobot.extras.models import Status


class Prefix(NautobotModel):
    """Prefix model for DiffSync."""

    _model = OrmPrefix
    _modelname = "prefix"
    _identifiers = (
        "network",
    )
    _attributes = (
        "prefix_length",
        "status__name",
    )

    network: str
    prefix_length: int
    status__name: str


class VirtualMachine(NautobotModel):
    """VirtualMachine model for DiffSync."""

    _model = OrmVirtualMachine
    _modelname = "virtual_machine"
    _identifiers = (
        "name",
        "cluster__name",
    )
    _attributes = (
        "vcpus",
        "memory",
        "disk",
        "status__name",
    )

    name: str
    cluster__name: str
    vcpus: Optional[int]
    memory: Optional[int]
    disk: Optional[int]
    status__name: str


class VMInterface(NautobotModel):
    """Interface model for DiffSync."""

    _model = OrmVMInterface
    _modelname = "vm_interface"
    _identifiers = (
        "name",
        "virtual_machine__name",
    )
    _attributes = (
        "status__name",
    )

    name: str
    virtual_machine__name: str
    status__name: str


class IPAddress(NautobotModel):
    """IPAddress model for DiffSync."""

    _model = OrmIPAddress
    _modelname = "ip_address"
    _identifiers = (
        "host",
    )
    _attributes = (
        "mask_length",
        "status__name",
    )

    host: str
    mask_length: str
    status__name: str


class IPAddressToInterface(NautobotModel):
    """IPAddress model for DiffSync."""

    _model = OrmIPAddressToInterface
    _modelname = "ip_address_to_interface"
    _identifiers = (
        "vm_interface__virtual_machine__name",
        "vm_interface__name",
    )
    _attributes = (
        "ip_address__host",
    )

    vm_interface__virtual_machine__name: str
    vm_interface__name: str
    ip_address__host: str


class DevicePrimaryIpAddress(DiffSyncModel):
    """IPAddress model for DiffSync."""

    _modelname = "device_primary_ip_address"
    _identifiers = (
        "virtual_machine",
        "ip_address",
    )
    _attributes = ()

    virtual_machine: str
    ip_address: str

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """
            Create IPAddress object in Nautobot.

            It will create the parent prefix from the provided host and netmask_length if it doesn't already exists
            It will set the virtual machine's primary_ip4 if attr 'is_primary' is present and set to True
            It will create an interface to IP association if the object:
            - has both virtual_machine and interface attributes provided
            - both objects exists in nautobot database
        """

        _virtual_machine = OrmVirtualMachine.objects.get(
            name=attrs["virtual_machine"]
        )
        _ip_address = OrmIPAddress.objects.get(
            address=attrs["ip_address"]
        )

        if _virtual_machine and _ip_address:
            _virtual_machine.primary_ip4 = _ip_address
            _virtual_machine.save()
        else:
            diffsync.job.logger.warning(f"Could not set virtual mùachine {attrs["virtual_machine"]} primary ip to {attrs["ip_address"]}")

        return super().create(ids=ids, diffsync=diffsync, attrs=attrs)
