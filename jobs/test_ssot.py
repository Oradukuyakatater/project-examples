from diffsync import DiffSync
from nautobot.apps.jobs import JSONVar, register_jobs
from nautobot.virtualization.models import VirtualMachine, VMInterface
from nautobot_ssot.jobs import DataSource

from .diffsync.adapters.nautobot import VirtualMachineNautobotAdapter
from .diffsync.adapters.remote import VirtualMachineRemoteAdapter


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
