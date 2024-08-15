from diffsync import DiffSync

from ..models.base import (
    Prefix as PrefixModel,
    VMInterface as VMInterfaceModel,
    VirtualMachine as VirtualMachineModel,
    IPAddress as IPAddressModel,
)

class VirtualMachineRemoteAdapter(DiffSync):
    """DiffSync adapter for remote system."""

    # prefix = PrefixModel
    vm_interface = VMInterfaceModel
    virtual_machine = VirtualMachineModel
    ip_address = IPAddressModel

    top_level = (
        # "prefix",
        "virtual_machine",
        "vm_interface",
        "ip_address",
    )

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
                    loaded_ip_address = self.ip_address(
                        host=address["ip"],
                        mask_length=address["mask"],
                        status__name=vm_interface.get("status", "Active"),
                        virtual_machine=virtual_machine["name"],
                        vm_interface=vm_interface["name"]
                    )
                    self.add(loaded_ip_address)
                    loaded_vm_interface.add_child(child=loaded_ip_address)
