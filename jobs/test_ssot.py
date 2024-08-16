from diffsync import DiffSync
from nautobot.apps.jobs import JSONVar, register_jobs
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
        super().run(dryrun=self.dryrun, memory_profiling=self.memory_profiling, *args, **kwargs)

    def load_source_adapter(self):
        self.source_adapter = VirtualMachineRemoteAdapter(data=self._data)
        self.source_adapter.load()

    def load_target_adapter(self):
        self.target_adapter = VirtualMachineNautobotAdapter(job=self)
        self.target_adapter.load()


register_jobs(VirtualMachineDataSource)


# test_data_overlapping_networks = [
#     {
#         "name": "vm-01",
#         "cluster": "esx-01",
#         "vcpus": 4,
#         "memory": 8192,
#         "disk": 200,
#         "interfaces": [
#             {
#                 "name": "eth0",
#                 "ip_addresses": [
#                     {
#                         "ip": "1.1.1.5",
#                         "mask": 24
#                     }
#                 ]
#             }
#         ]
#     },
#     {
#         "name": "vm-02",
#         "cluster": "esx-01",
#         "vcpus": 4,
#         "memory": 8192,
#         "disk": 200,
#         "interfaces": [
#             {
#                 "name": "eth0",
#                 "ip_addresses": [
#                     {
#                         "ip": "1.1.1.5",
#                         "mask": 23
#                     }
#                 ]
#             }
#         ]
#     }
# ]
