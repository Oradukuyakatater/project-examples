# example_ssot_app/jobs.py
from typing import Optional

from diffsync import DiffSync
from nautobot.ipam.models import VLAN
from nautobot.apps.jobs import Job, JSONVar, register_jobs
from nautobot_ssot.contrib import NautobotModel, NautobotAdapter
from nautobot_ssot.jobs import DataSource


class VLANModel(NautobotModel):
    """DiffSync model for VLANs."""
    _model = VLAN
    _modelname = "vlan"
    _identifiers = ("vid", "group__name")
    _attributes = ("description",)

    vid: int
    group__name: Optional[str] = None
    description: Optional[str] = None


class MySSoTNautobotAdapter(NautobotAdapter):
    """DiffSync adapter for Nautobot."""
    vlan = VLANModel
    top_level = ("vlan",)


class MySSoTRemoteAdapter(DiffSync):
    """DiffSync adapter for remote system."""
    vlan = VLANModel
    top_level = ("vlan",)

    def __init__(self, *args, data, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data

    def load(self):
        for vlan in self._data:
            loaded_vlan = self.vlan(vid=vlan["vlan_id"], group__name=vlan["grouping"], description=vlan["description"])
            self.add(loaded_vlan)


class ExampleDataSource(DataSource, Job):
    """SSoT Job class."""
    class Meta:
        name = "Example Data Source"

    source_data = JSONVar()

    def run(self, dryrun, memory_profiling, source_data, *args, **kwargs):
        self._data = source_data
        super().run(dryrun, memory_profiling, args, kwargs)

    def load_source_adapter(self):
        self.source_adapter = MySSoTRemoteAdapter(self._data)
        self.source_adapter.load()

    def load_target_adapter(self):
        self.target_adapter = MySSoTNautobotAdapter()
        self.target_adapter.load()


register_jobs(ExampleDataSource)
