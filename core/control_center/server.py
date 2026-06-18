from core.runtime.event_bus import subscribe

live_events = []


def push_event(event):
    live_events.append(event)


def get_live_events():
    return live_events


subscribe("proposal_batch", push_event)
subscribe("task_queued", push_event)