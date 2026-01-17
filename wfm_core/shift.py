from datetime import time

def _round_minutes_to_quarter_hours(minutes: int) -> float:
    return round(minutes / 15) * 15 / 60.0

class Shift:
    def __init__(self, staff_id, date, start_time, end_time):
        if not isinstance(staff_id, int) or isinstance(staff_id, bool):
            raise TypeError(f"staff_id must be an integer, got {type(staff_id)}")
        if staff_id < 1:
            raise ValueError("staff_id must be ≥ 1")

        if not isinstance(start_time, time) or not isinstance(end_time, time):
            raise TypeError("start_time and end_time must be datetime.time objects")
        if start_time >= end_time:
            raise ValueError("start_time must be before end_time")

        self.staff_id = staff_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

        duration_minutes = self._get_actual_duration_minutes()
        if duration_minutes < 60 or duration_minutes > 12 * 60:
            raise ValueError("duration must be between 1 and 12 hours")

        self.duration_hours = _round_minutes_to_quarter_hours(duration_minutes)

    def _get_actual_duration_minutes(self):
        start = self.start_time.hour * 60 + self.start_time.minute
        end = self.end_time.hour * 60 + self.end_time.minute
        return end - start

