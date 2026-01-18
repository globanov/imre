from datetime import datetime, timedelta

from .models import WeeklyWorkload


def _get_week_start(date_str: str) -> str:
    """Return ISO week start (Monday) for given date."""
    dt = datetime.fromisoformat(date_str)
    week_start = dt - timedelta(days=dt.weekday())
    return week_start.strftime("%Y-%m-%d")


def handle_shift_created(event) -> None:
    """Update WeeklyWorkload in DB based on ShiftCreated event."""
    from wfm_core.events import ShiftCreated

    if not isinstance(event, ShiftCreated):
        raise TypeError("Expected ShiftCreated event")

    week_start_str = _get_week_start(event.date)
    workload, created = WeeklyWorkload.objects.get_or_create(
        staff_id=event.staff_id, week_start=week_start_str, defaults={"total_hours": 0.0}
    )
    workload.total_hours += event.duration_hours
    workload.save(update_fields=["total_hours"])
