from ..models.base import (
    Prefix as PrefixModel,
    VMInterface as VMInterfaceModel,
    VirtualMachine as VirtualMachineModel,
    IPAddress as IPAddressModel,
)
from nautobot_ssot.contrib import NautobotAdapter


class VirtualMachineNautobotAdapter(NautobotAdapter):
    """DiffSync adapter for Nautobot."""

    virtual_machine = VirtualMachineModel
    top_level = ("virtual_machine",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
