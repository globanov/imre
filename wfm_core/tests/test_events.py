from wfm_core.events import ShiftCreated


def test_shift_created_event():
    event = ShiftCreated(
        staff_id=17, date="2026-06-15", start_time="09:00", end_time="18:00", duration_hours=9.0
    )
    assert event.staff_id == 17
    assert event.date == "2026-06-15"
    assert event.start_time == "09:00"
    assert event.end_time == "18:00"
    assert event.duration_hours == 9.0
