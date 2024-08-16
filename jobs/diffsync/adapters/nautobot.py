from ..models.base import (
    Prefix as PrefixModel,
    VMInterface as VMInterfaceModel,
    VirtualMachine as VirtualMachineModel,
    IPAddress as IPAddressModel,
    IPAddressToInterface as IPAddressToInterfaceModel,
    DevicePrimaryIpAddress as DevicePrimaryIpAddressModel,
)
from nautobot_ssot.contrib import NautobotAdapter


class VirtualMachineNautobotAdapter(NautobotAdapter):
    """DiffSync adapter for Nautobot."""

    prefix = PrefixModel
    virtual_machine = VirtualMachineModel
    vm_interface = VMInterfaceModel
    ip_address = IPAddressModel
    ip_address_to_interface = IPAddressToInterfaceModel
    device_primary_ip_address = DevicePrimaryIpAddressModel

    top_level = (
        "prefix",
        "ip_address",
        "virtual_machine",
        "vm_interface",
        "ip_address_to_interface",
        "device_primary_ip_address",
    )

    def __init__(self, *args, data, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data
