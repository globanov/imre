# wfm_core/tests/test_shift.py
from datetime import time

import pytest
from wfm_core.shift import Shift


def test_staff_id_must_be_integer():
    with pytest.raises(TypeError):
        Shift(staff_id="1", date="2026-06-15", start_time=time(9), end_time=time(10))
    with pytest.raises(TypeError):
        Shift(staff_id=1.0, date="2026-06-15", start_time=time(9), end_time=time(10))
    with pytest.raises(TypeError):
        Shift(staff_id=True, date="2026-06-15", start_time=time(9), end_time=time(10))


def test_staff_id_must_be_positive():
    with pytest.raises(ValueError):
        Shift(staff_id=0, date="2026-06-15", start_time=time(9), end_time=time(10))
    with pytest.raises(ValueError):
        Shift(staff_id=-1, date="2026-06-15", start_time=time(9), end_time=time(10))
    with pytest.raises(ValueError):
        Shift(staff_id=-42, date="2026-06-15", start_time=time(9), end_time=time(10))


def test_valid_staff_id():
    shift = Shift(staff_id=1, date="2026-06-15", start_time=time(9), end_time=time(10))
    assert shift.staff_id == 1

    shift = Shift(staff_id=42, date="2026-06-15", start_time=time(9), end_time=time(10))
    assert shift.staff_id == 42

def test_start_time_must_be_before_end_time():
    with pytest.raises(ValueError, match="start_time must be before end_time"):
        Shift(staff_id=1, date="2026-06-15", start_time=time(18, 0), end_time=time(9, 0))

def test_valid_time_range():
    shift = Shift(staff_id=1, date="2026-06-15", start_time=time(9, 0), end_time=time(18, 0))
    assert shift.start_time == time(9, 0)
    assert shift.end_time == time(18, 0)

def test_shift_duration_must_be_at_least_1_hour():
    with pytest.raises(ValueError, match="duration must be between 1 and 12 hours"):
        Shift(staff_id=1, date="2026-06-15", start_time=time(9, 0), end_time=time(9, 59))

def test_shift_duration_cannot_exceed_12_hours():
    with pytest.raises(ValueError, match="duration must be between 1 and 12 hours"):
        Shift(staff_id=1, date="2026-06-15", start_time=time(0, 0), end_time=time(12, 1))

def test_valid_1_hour_shift():
    shift = Shift(staff_id=1, date="2026-06-15", start_time=time(9, 0), end_time=time(10, 0))
    assert shift.duration_hours == 1.0

def test_valid_12_hour_shift():
    shift = Shift(staff_id=1, date="2026-06-15", start_time=time(8, 0), end_time=time(20, 0))
    assert shift.duration_hours == 12.0

def test_duration_rounded_to_15_minutes():
    shift = Shift(staff_id=1, date="2026-06-15", start_time=time(9, 10), end_time=time(10, 20))
    assert shift.duration_hours == 1.25  # 1ч 10мин → 1.25ч

    shift2 = Shift(staff_id=1, date="2026-06-15", start_time=time(14, 5), end_time=time(16, 50))
    assert shift2.duration_hours == 2.75  # 2ч 45мин → 2.75ч