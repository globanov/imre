from wfm_core.weekly_workload import WeeklyWorkload


def test_create_weekly_workload():
    workload = WeeklyWorkload(staff_id=17, week_start="2026-06-15")
    assert workload.staff_id == 17
    assert workload.week_start == "2026-06-15"
    assert workload.total_hours == 0.0


def test_add_shift_duration():
    workload = WeeklyWorkload(staff_id=17, week_start="2026-06-15")
    workload.add_shift_duration(9.0)
    assert workload.total_hours == 9.0


def test_add_multiple_shifts():
    workload = WeeklyWorkload(staff_id=17, week_start="2026-06-15")
    workload.add_shift_duration(9.0)
    workload.add_shift_duration(4.5)
    assert workload.total_hours == 13.5
