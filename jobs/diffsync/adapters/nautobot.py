from ..models.base import (
    Prefix as PrefixModel,
    VMInterface as VMInterfaceModel,
    VirtualMachine as VirtualMachineModel,
    IPAddress as IPAddressModel,
    IPAddressToInterface as IPAddressToInterfaceModel,
)
from nautobot_ssot.contrib import NautobotAdapter


class VirtualMachineNautobotAdapter(NautobotAdapter):
    """DiffSync adapter for Nautobot."""

    prefix = PrefixModel
    virtual_machine = VirtualMachineModel
    vm_interface = VMInterfaceModel
    ip_address = IPAddressModel
    ip_address_to_interface = IPAddressToInterfaceModel

    top_level = (
        "prefix",
        "virtual_machine",
        "vm_interface",
        "ip_address",
        "ip_address_to_interface",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
