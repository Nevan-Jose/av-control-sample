"""Loads the two data files.

These JSON files stand in for the two spreadsheets: "Spreadsheet A" (the AV
equipment list) and "Spreadsheet B" (the staff shift schedule). No Streamlit
imports here.
"""
import json
from pathlib import Path

# data/ sits next to core/, one level up from this file.
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_json(filename: str) -> list[dict]:
    """Read a JSON file from the data folder into a list of dicts.

    If the file is missing, Python raises FileNotFoundError on its own, which is
    fine here.
    """
    with open(_DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def load_equipment() -> list[dict]:
    """Loads data/equipment.json. Each row has the fields from DATA.md section 2:
    device_id, name, type, room, status, last_serviced."""
    return _load_json("equipment.json")


def load_schedules() -> list[dict]:
    """Loads data/schedules.json. Each row has the fields from DATA.md section 3:
    staff_name, role, shift_date, time_block, assigned_location."""
    return _load_json("schedules.json")
