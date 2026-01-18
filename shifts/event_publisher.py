from wfm_core.worker import handle_shift_created


def publish(event):
    """Publish event to subscribers (currently sync)."""
    handle_shift_created(event)
