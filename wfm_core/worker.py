from datetime import datetime, timedelta

from wfm_core.events import ShiftCreated
from wfm_core.weekly_workload import WeeklyWorkload

# In-memory storage (replace with DB later)
workload_store: dict[tuple[int, str], WeeklyWorkload] = {}


def _get_week_start(date_str: str) -> str:
    """Return ISO week start (Monday) for given date."""
    dt = datetime.fromisoformat(date_str)
    # Monday is 0 in ISO weekday
    week_start = dt - timedelta(days=dt.weekday())
    return week_start.strftime("%Y-%m-%d")


def handle_shift_created(event: ShiftCreated) -> None:
    """Update WeeklyWorkload based on ShiftCreated event."""
    week_start = _get_week_start(event.date)
    key = (event.staff_id, week_start)

    if key not in workload_store:
        workload_store[key] = WeeklyWorkload(staff_id=event.staff_id, week_start=week_start)

    workload_store[key].add_shift_duration(event.duration_hours)
