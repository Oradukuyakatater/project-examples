from nautobot.apps.jobs import Job, register_jobs

class Test(Job):
    """SSoT Job class."""
    class Meta:
        name = "Test Job"

    def run(self):
        return True

register_jobs(Test)
