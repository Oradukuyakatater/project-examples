from diffsync import DiffSyncModel
from typing import List, Optional

from nautobot_ssot.contrib import NautobotModel

from nautobot.ipam.models import IPAddress, Prefix
from nautobot.virtualization.models import VirtualMachine, VMInterface


class Prefix(NautobotModel):
    """Prefix model for DiffSync."""

    _model = Prefix
    _modelname = "prefix"
    _identifiers = (
        "prefix",
    )
    _attributes = (
        "status__name"
    )

    prefix: str
    status__name: str


class VirtualMachine(NautobotModel):
    """VirtualMachine model for DiffSync."""

    _model = VirtualMachine
    _modelname = "virtual_machine"
    _identifiers = (
        "name",
        "cluster__name",
    )
    _attributes = (
        "vcpus",
        "memory",
        "disk",
        "status__name"
    )
    _children = {
        "vm_interface": "vm_interfaces",
    }

    name: str
    cluster__name: str
    vcpus: Optional[int]
    memory: Optional[int]
    disk: Optional[int]
    status__name: str
    vm_interfaces: Optional[List["VMInterface"]] = []


class VMInterface(NautobotModel):
    """Interface model for DiffSync."""

    _model = VMInterface
    _modelname = "vm_interface"
    _identifiers = (
        "name",
        "virtual_machine__name",
    )
    _attributes = ("status__name")

    name: str
    virtual_machine__name: str
    status__name: str


class IPAddress(NautobotModel):
    """IPAddress model for DiffSync."""

    _model = IPAddress
    _modelname = "ip_address"
    _identifiers = (
        "host",
        "mask_length",
    )
    _attributes = (
        "status__name",
        "description",
        "virtual_machine",
        "vm_interface",
    )

    host: str
    mask_length: str
    status__name: str
    vm_interfaces: Optional[List[str]] = list()
