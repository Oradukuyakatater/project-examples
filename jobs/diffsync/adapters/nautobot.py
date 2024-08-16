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
        "virtual_machine",
        "vm_interface",
        "ip_address",
        "ip_address_to_interface",
    )

    def __init__(self, *args, data, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data

    def load(self):
        super().load()
        self.top_level = self.top_level + ("device_primary_ip_address", )
        for virtual_machine in self._data:
            for vm_interface in virtual_machine["interfaces"]:
                for address in vm_interface.get("ip_addresses", []):
                    if address["primary"]:
                        loaded_device_primary_ip_address = self.device_primary_ip_address(
                            virtual_machine=virtual_machine["name"],
                            ip_address=f"{address['ip']}/{address['mask']}",
                        )
                        self.add(loaded_device_primary_ip_address)
