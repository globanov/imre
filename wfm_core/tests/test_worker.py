from django.test import TestCase

from wfm_core.events import ShiftCreated
from wfm_core.worker import handle_shift_created, workload_store


class WorkerTest(TestCase):
    def tearDown(self):
        workload_store.clear()

    def test_handle_shift_created_updates_weekly_workload(self):
        event = ShiftCreated(
            staff_id=17,
            date="2026-06-15",  # Monday
            start_time="09:00",
            end_time="18:00",
            duration_hours=9.0,
        )

        handle_shift_created(event)

        key = (17, "2026-06-15")
        assert key in workload_store
        assert workload_store[key].total_hours == 9.0

    def test_handle_multiple_shifts_same_week(self):
        event1 = ShiftCreated(17, "2026-06-15", "09:00", "18:00", 9.0)  # Mon
        event2 = ShiftCreated(17, "2026-06-16", "10:00", "14:30", 4.5)  # Tue

        handle_shift_created(event1)
        handle_shift_created(event2)

        key = (17, "2026-06-15")
        assert workload_store[key].total_hours == 13.5
