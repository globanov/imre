from dataclasses import dataclass


@dataclass(frozen=True)
class ShiftCreated:
    staff_id: int
    date: str
    start_time: str
    end_time: str
    duration_hours: float
