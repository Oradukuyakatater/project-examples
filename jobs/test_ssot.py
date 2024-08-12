from diffsync import DiffSync
from nautobot.apps.jobs import JSONVar, register_jobs
from nautobot.virtualization.models import VirtualMachine
from nautobot_ssot.jobs import DataSource
from nautobot_ssot.contrib import NautobotAdapter, NautobotModel


class VirtualMachineModel(NautobotModel):
    """DiffSync model for VLANs."""

    _model = VirtualMachine
    _modelname = "virtual_machine"
    _identifiers = ("name", "cluster__name", )
    _attributes = ()

    name: str
    cluster__name: str


class VirtualMachineNautobotAdapter(NautobotAdapter):
    """DiffSync adapter for Nautobot."""

    virtual_machine = VirtualMachineModel
    top_level = ("virtual_machine",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualMachineRemoteAdapter(DiffSync):
    """DiffSync adapter for remote system."""

    virtual_machine = VirtualMachineModel
    top_level = ("virtual_machine",)

    def __init__(self, *args, data, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data

    def load(self):
        # for virtual_machine in self._sql_connection.query(self._query):
        for virtual_machine in self._data:
            loaded_virtual_machine = self.virtual_machine(name=virtual_machine["name"], cluster__name=virtual_machine["cluster"])
            self.add(loaded_virtual_machine)


class VirtualMachineDataSource(DataSource):
    """SSoT Job class."""

    source_data = JSONVar()

    class Meta:
        name = "Virtual Machine Data Source"

    def run(self, dryrun, memory_profiling, source_data, *args, **kwargs):
        self._data = source_data
        self.dryrun = dryrun
        self.memory_profiling = memory_profiling
        self.logger.info(f"dryrun value: {self.dryrun}")
        self.logger.info(f"source data value: {self._data}")
        super().run(dryrun=self.dryrun, memory_profiling=self.memory_profiling, *args, **kwargs)

    def load_source_adapter(self):
        self.source_adapter = VirtualMachineRemoteAdapter(data=self._data)
        self.source_adapter.load()

    def load_target_adapter(self):
        self.target_adapter = VirtualMachineNautobotAdapter(job=self)
        self.target_adapter.load()


register_jobs(VirtualMachineDataSource)
