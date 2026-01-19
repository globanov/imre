# Shift Specification

## Fields
- `staff_id`: int
- `date`: str "YYYY-MM-DD" — **start date of the shift**
- `start_time`: str "HH:MM"
- `end_time`: str "HH:MM"

## Rules
- **Single-day shift**: `start_time` and `end_time` must be on the same calendar day (`end_time > start_time`)
- **Duration**: between 1 and 12 hours, rounded to 15 minutes (0.25 hours)
- **Time format**: 24-hour, e.g., "09:00", "18:30"

## Examples
✅ Valid:
- `date: "2026-06-15", start: "09:00", end: "18:00"` → 9h
- `date: "2026-06-15", start: "14:00", end: "18:15"` → 4.25h

❌ Invalid:
- `start: "22:00", end: "06:00"` → crosses midnight (not supported)
- `duration < 1h` or `> 12h`
- `end_time <= start_time`
