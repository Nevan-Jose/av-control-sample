"""Tests for core.insights: small helpers that work over the two data sets.

This is the logic behind the numbers at the top of the screen and the "who is on
shift in this device's room" note. Like the rest of core/, it is plain Python
with no Streamlit, written test first.
"""
from core.data import load_equipment, load_schedules
from core.insights import equipment_summary, staff_for_location, staff_on_date


def test_equipment_summary_counts():
    summary = equipment_summary(load_equipment())
    assert summary == {"total": 4, "online": 3, "offline": 1}


def test_equipment_summary_empty():
    assert equipment_summary([]) == {"total": 0, "online": 0, "offline": 0}


def test_staff_for_location_matches_room():
    # Joins equipment.room <-> schedule.assigned_location
    schedules = load_schedules()
    dibner = staff_for_location(schedules, "Dibner Hall 101")
    assert [s["staff_name"] for s in dibner] == ["Jordan Lee"]


def test_staff_for_location_no_match_returns_empty():
    # display_3's room (370 Jay St Conf Room A) has nobody scheduled.
    assert staff_for_location(load_schedules(), "370 Jay St Conf Room A") == []


def test_staff_on_date_filters_by_shift_date():
    on_22 = staff_on_date(load_schedules(), "2026-06-22")
    assert {s["staff_name"] for s in on_22} == {"Jordan Lee", "Sam Patel"}
    on_23 = staff_on_date(load_schedules(), "2026-06-23")
    assert {s["staff_name"] for s in on_23} == {"Priya Nair"}
