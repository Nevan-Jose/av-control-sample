"""Small helpers that work over the two data sets.

These power the row of numbers at the top of the screen and the "who is on shift
in this device's room" note. That note connects the two data sources instead of
just showing them side by side. These are plain functions with no Streamlit
imports, so they are easy to test.
"""


def equipment_summary(equipment: list[dict]) -> dict:
    """Counts for the top of the screen: total devices, and how many are online
    versus offline."""
    total = len(equipment)
    online = sum(1 for e in equipment if e.get("status") == "online")
    return {"total": total, "online": online, "offline": total - online}


def staff_for_location(schedules: list[dict], location: str) -> list[dict]:
    """Schedule rows where assigned_location matches the given location.

    This matches a device's room against the staff scheduled there, so the
    screen can show who is on shift in that room."""
    return [s for s in schedules if s.get("assigned_location") == location]


def staff_on_date(schedules: list[dict], date: str) -> list[dict]:
    """Schedule rows where shift_date matches the given date (YYYY-MM-DD)."""
    return [s for s in schedules if s.get("shift_date") == date]
