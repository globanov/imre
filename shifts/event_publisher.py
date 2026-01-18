from .worker import handle_shift_created


def publish(event):
    """Publish event to subscribers (sync DB update)."""
    handle_shift_created(event)
