import ipaddress

from diffsync import DiffSyncModel
from typing import List, Optional, Union

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
        "primary_ip4__host",
        "primary_ip4__mask_length",
    )

    name: str
    cluster__name: str
    vcpus: Optional[int]
    memory: Optional[int]
    disk: Optional[int]
    status__name: str
    primary_ip4__host: Optional[str]
    primary_ip4__mask_length: Optional[int]


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
        "ip_address__host",
    )
    _attributes = ()

    vm_interface__virtual_machine__name: str
    vm_interface__name: str
    ip_address__host: str


class VirtualMachinePrimaryIP4(NautobotModel):
    """VirtualMachine model for DiffSync."""

    _model = OrmVirtualMachine
    _modelname = "virtual_machine_primary_ip4"
    _identifiers = (
        "name",
        "cluster__name",
    )
    _attributes = (
        "primary_ip4__host",
        "primary_ip4__mask_length",
    )
    name: str
    cluster__name: str
    primary_ip4__host: Optional[str]
    primary_ip4__mask_length: Optional[int]
