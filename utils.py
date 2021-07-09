"""Utility functions."""
from kytos.core.events import KytosEvent


def emit_event(controller, name, **kwargs):
    """Send an event when something happens with an EVC."""
    event_name = f'kytos/mef_eline.{name}'
    event = KytosEvent(name=event_name, content=kwargs)
    controller.buffers.app.put(event)
