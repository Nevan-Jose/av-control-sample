"""Tests for core.data: the loaders for the two mock JSON files.

Per CONTRACTS.md and DATA.md sections 2 and 3, the loaders return lists of dicts
with an exact set of fields and nothing extra.
"""
from core.data import load_equipment, load_schedules

EQUIPMENT_FIELDS = {"device_id", "name", "type", "room", "status", "last_serviced"}
SCHEDULE_FIELDS = {"staff_name", "role", "shift_date", "time_block", "assigned_location"}


def test_load_equipment_returns_list_of_dicts():
    equipment = load_equipment()
    assert isinstance(equipment, list)
    assert len(equipment) == 4
    assert all(isinstance(row, dict) for row in equipment)


def test_equipment_rows_have_exactly_the_data_md_fields():
    for row in load_equipment():
        assert set(row.keys()) == EQUIPMENT_FIELDS


def test_equipment_contains_known_device():
    by_id = {row["device_id"]: row for row in load_equipment()}
    assert "projector_1" in by_id
    assert by_id["projector_1"]["name"] == "Epson Pro L730U"
    assert by_id["projector_1"]["type"] == "projector"


def test_load_schedules_returns_list_of_dicts():
    schedules = load_schedules()
    assert isinstance(schedules, list)
    assert len(schedules) == 3
    assert all(isinstance(row, dict) for row in schedules)


def test_schedule_rows_have_exactly_the_data_md_fields():
    for row in load_schedules():
        assert set(row.keys()) == SCHEDULE_FIELDS


def test_schedules_contains_known_staff():
    names = {row["staff_name"] for row in load_schedules()}
    assert {"Jordan Lee", "Sam Patel", "Priya Nair"} == names
