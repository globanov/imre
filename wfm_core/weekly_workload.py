class WeeklyWorkload:
    def __init__(self, staff_id: int, week_start: str):
        if not isinstance(staff_id, int) or staff_id < 1:
            raise ValueError("staff_id must be a positive integer")
        self.staff_id = staff_id
        self.week_start = week_start
        self.total_hours = 0.0

    def add_shift_duration(self, hours: float):
        if hours <= 0:
            raise ValueError("hours must be positive")
        self.total_hours += hours
