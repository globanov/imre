# Specification: Shift

A shift is a period during which a staff member works on a specific date.

## Attributes
- `staff_id`: integer ≥ 1
- `date`: ISO date (YYYY-MM-DD)
- `start_time`: start time (HH:MM)
- `end_time`: end time (HH:MM)

## Rules
1. **Duration**: between 1 and 12 hours, rounded to 15 minutes (0.25 hours).
2. **Time**: `start_time` < `end_time`, both belong to the same day (`date`).