"""Module responsible to handle schedules."""
import time
from sched import scheduler
from kytos.core.helpers import now


class Schedule:
    """Schedule events."""

    def __init__(self):
        """Initialize the schedule structure."""
        self.scheduler = scheduler(time.time, time.sleep)

    def run_pending(self):
        """Verify schedule and execute pended events."""
        self.scheduler.run(False)
        time.sleep(1)

    def circuit_deploy(self, circuit):
        """Add a new circuit deploy event."""
        seconds = (circuit.creation_time - now()).total_seconds()
        self.scheduler.enter(seconds, 1, circuit.deploy)
