# Weekly Workload Specification

## Purpose
Track total scheduled shift duration per staff member per week for reporting and compliance.

## Key Rules
- **Week**: ISO week (Monday–Sunday)
- **Key**: `(staff_id: int, week_start: str "YYYY-MM-DD")`
- **Value**: `total_hours: float` — sum of all shift durations in the week, rounded to 0.25h
- **Update**: asynchronous, triggered by `ShiftCreated` event
- **Idempotent**: processing the same event twice must not change result

## Example
Given:
- Shift 1: 2026-06-15 (Mon), 09:00–18:00 → 9.0h
- Shift 2: 2026-06-16 (Tue), 10:00–14:30 → 4.5h

Then:
- Week start: 2026-06-15
- Total: 9.0 + 4.5 = **13.5 hours**