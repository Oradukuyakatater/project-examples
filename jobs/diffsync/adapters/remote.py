import ipaddress

from diffsync import DiffSync

from ..models.base import (
    Prefix as PrefixModel,
    VMInterface as VMInterfaceModel,
    VirtualMachine as VirtualMachineModel,
    IPAddress as IPAddressModel,
    IPAddressToInterface as IPAddressToInterfaceModel,
    DevicePrimaryIpAddress as DevicePrimaryIpAddressModel,
)

class VirtualMachineRemoteAdapter(DiffSync):
    """DiffSync adapter for remote system."""

    prefix = PrefixModel
    vm_interface = VMInterfaceModel
    virtual_machine = VirtualMachineModel
    ip_address = IPAddressModel
    ip_address_to_interface = IPAddressToInterfaceModel
    device_primary_ip_address = DevicePrimaryIpAddressModel

    top_level = (
        "prefix",
        "virtual_machine",
        "vm_interface",
        "ip_address",
        "ip_address_to_interface",
        "device_primary_ip_address",
    )

    prefixes_local = []

    def __init__(self, *args, data, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data

    def load(self):
        # for virtual_machine in self._sql_connection.query(self._query):
        for virtual_machine in self._data:
            loaded_virtual_machine = self.virtual_machine(
                name=virtual_machine["name"],
                cluster__name=virtual_machine["cluster"],
                vcpus=virtual_machine.get("vcpus"),
                memory=virtual_machine.get("memory"),
                disk=virtual_machine.get("disk"),
                status__name=virtual_machine.get("status", "Active")
            )
            self.add(loaded_virtual_machine)
            for vm_interface in virtual_machine["interfaces"]:
                loaded_vm_interface = self.vm_interface(
                    name=vm_interface["name"],
                    virtual_machine__name=virtual_machine["name"],
                    status__name=vm_interface.get("status", "Active")
                )
                self.add(loaded_vm_interface)

                for address in vm_interface.get("ip_addresses", []):
                    network_obj = ipaddress.IPv4Network(f"{address['ip']}/{address['mask']}", strict=False)
                    if network_obj.with_prefixlen not in self.prefixes_local:
                        loaded_prefix = self.prefix(
                            network=str(network_obj.network_address),
                            prefix_length=network_obj.prefixlen,
                            status__name=vm_interface.get("status", "Active")
                        )
                        self.add(loaded_prefix)
                        self.prefixes_local.append(network_obj.with_prefixlen)
                    loaded_ip_address = self.ip_address(
                        host=address["ip"],
                        mask_length=address["mask"],
                        status__name=vm_interface.get("status", "Active"),
                        virtual_machine=virtual_machine["name"],
                        vm_interface=vm_interface["name"]
                    )
                    self.add(loaded_ip_address)
                    loaded_ip_address_to_interface = self.ip_address_to_interface(
                        vm_interface__virtual_machine__name=virtual_machine["name"],
                        vm_interface__name=vm_interface["name"],
                        ip_address__host=address["ip"],
                    )
                    self.add(loaded_ip_address_to_interface)
                    if address["primary"]:
                        loaded_device_primary_ip_address = self.device_primary_ip_address(
                            name=virtual_machine["name"],
                            primary_ip4__address=f"{address['ip']}/{address['mask']}",
                        )
                        self.add(loaded_device_primary_ip_address)
