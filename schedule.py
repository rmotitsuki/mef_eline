"""Module responsible to handle schedules."""
import time
from sched import scheduler
from kytos.core.helpers import now
from kytos.core import log


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

        if not circuit.enabled:
            log.debug(f'{circuit.id} is not enabled')
        elif not circuit.active:
            log.debug(f'{circuit.id} is not active')
        elif circuit.enabled and not circuit.active:
            self.scheduler.enter(seconds, circuit.priority, circuit.deploy)
            log.debug(f'{circuit.id} scheduled to be activated.')
