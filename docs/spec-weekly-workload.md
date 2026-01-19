# Weekly Workload Specification

## Key Rules
- **Week**: ISO week (Monday–Sunday)
- **Key**: `(staff_id: int, week_start: str "YYYY-MM-DD")`
- **Value**: `total_hours: float` — sum of all shift durations in the week, rounded to 0.25h
- **Update**: synchronous, triggered by `ShiftCreated` event
- **Idempotent**: not implemented (technical debt)

## Example
Given:
- Shift 1: 2026-06-15 (Mon), 09:00–18:00 → 9.0h
- Shift 2: 2026-06-16 (Tue), 10:00–14:30 → 4.5h

Then:
- Week start: 2026-06-15
- Total: 9.0 + 4.5 = **13.5 hours**

## Update Mechanism
- **Trigger**: `ShiftCreated` event (published on shift creation)
- **Processing**: **synchronous**, in the same HTTP request
- **Atomicity**: update happens in the same database transaction as shift creation
- **Idempotency**: not implemented (technical debt — see Roadmap)

## Read API
- `GET /api/workload/staff/{staff_id}/week/{date}`
- Normalizes `{date}` to week start (Monday)
- Returns 404 if no shifts recorded for that week
