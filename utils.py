"""Utility functions."""
from kytos.core.events import KytosEvent


def map_evc_event_content(evc, **kwargs):
    """Returns a set of values from evc to be used for content"""
    return kwargs | {"evc_id": evc.id,
                     "name": evc.name,
                     "metadata": evc.metadata,
                     "active": evc._active,
                     "enabled": evc._enabled,
                     "uni_a": evc.uni_a.as_dict(),
                     "uni_z": evc.uni_z.as_dict()}


def emit_event(controller, name, context="kytos/mef_eline", content=None):
    """Send an event when something happens with an EVC."""
    event_name = f"{context}.{name}"
    event = KytosEvent(name=event_name, content=content)
    controller.buffers.app.put(event)


def notify_link_available_tags(controller, link, src_func=None):
    """Notify link available tags."""
    emit_event(controller, "link_available_tags", content={
        "link": link,
        "src_func": src_func
    })


def compare_endpoint_trace(endpoint, vlan, trace):
    """Compare and endpoint with a trace step."""
    if vlan and "vlan" in trace:
        return (
            endpoint.switch.dpid == trace["dpid"]
            and endpoint.port_number == trace["port"]
            and vlan == trace["vlan"]
        )
    return (
        endpoint.switch.dpid == trace["dpid"]
        and endpoint.port_number == trace["port"]
    )


def compare_uni_out_trace(uni, trace):
    """Check if the trace last step (output) matches the UNI attributes."""
    # keep compatibility for old versions of sdntrace-cp
    if "out" not in trace:
        return True
    if not isinstance(trace["out"], dict):
        return False
    uni_vlan = uni.user_tag.value if uni.user_tag else None
    return (
        uni.interface.port_number == trace["out"].get("port")
        and uni_vlan == trace["out"].get("vlan")
    )
