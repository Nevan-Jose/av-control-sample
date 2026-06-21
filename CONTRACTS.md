# CONTRACTS: Fixed Function Shapes

These are the function shapes that, once their tests pass, should not change for
the rest of the build. If a later step seems to need a different shape, stop and
rethink the step, not the contract.

The reason for fixing them is simple: it keeps the `core/` logic and the `app.py`
screen from drifting apart as the build goes on.

## core/auth.py

```python
from enum import Enum

class Role(str, Enum):
    TECHNICIAN = "TECHNICIAN"
    MANAGER = "MANAGER"

# name -> Role, per DATA.md section 1
USERS: dict[str, Role]

def get_role(user_name: str) -> Role | None:
    """Find the role for a user name. Returns None if it is not recognized."""

def can_trigger_command(role: Role) -> bool:
    """True only for MANAGER. This is the one place the role rule lives. The
    screen (to show or hide the panel) and the action (to actually block it)
    both call this instead of repeating the check."""
```

## core/data.py

```python
def load_equipment() -> list[dict]:
    """Loads data/equipment.json. Each dict has the fields from DATA.md
    section 2: device_id, name, type, room, status, last_serviced."""

def load_schedules() -> list[dict]:
    """Loads data/schedules.json. Each dict has the fields from DATA.md
    section 3: staff_name, role, shift_date, time_block, assigned_location."""
```

If a JSON file is missing, Python raises FileNotFoundError on its own. No custom
error types are needed at this size.

## core/payload.py

```python
from datetime import datetime

VALID_COMMANDS = {"power_on", "power_off", "input_select", "mute"}

def build_command_payload(
    device_id: str,
    command: str,
    triggered_by: str,
) -> dict:
    """
    Builds the JSON command. Raises ValueError if command is not in
    VALID_COMMANDS.

    Returns exactly:
    {
        "command": <command>,
        "device": <device_id>,
        "triggered_by": <triggered_by>,
        "timestamp": <ISO 8601 string, UTC>
    }

    This is the example from the job post ({"command": "power_on", "device":
    "projector_1"}) plus two fields (triggered_by, timestamp) so the history
    makes sense. Do not add more fields without updating this file first.
    """
```

This function does not check roles. That is core.auth's job. app.py calls
can_trigger_command(role) before it ever calls build_command_payload. Keeping
these apart makes each one easy to test on its own.

## core/insights.py (added later for the dashboard)

Plain helpers that work over the loaded data. Added after the core build to
support the top numbers and the "who is on shift in this room" note. They take
lists that are already loaded (they do not read files), so they work with
core.data without depending on it.

```python
def equipment_summary(equipment: list[dict]) -> dict:
    """Returns {"total": int, "online": int, "offline": int}."""

def staff_for_location(schedules: list[dict], location: str) -> list[dict]:
    """Schedule rows where assigned_location == location. Matches a device's
    room to the staff scheduled there."""

def staff_on_date(schedules: list[dict], date: str) -> list[dict]:
    """Schedule rows where shift_date == date (YYYY-MM-DD)."""
```

Like the rest of `core/`, this has no Streamlit imports and is covered by tests
in tests/test_insights.py.

## The screen (app.py): how it should behave

- Use core.auth.get_role for login. Do not redo role lookup by hand.
- Show the Equipment and Schedule tables for both roles.
- Only show the Device Control panel when can_trigger_command(role) is True.
- On send, call core.payload.build_command_payload(...). Never build the JSON by
  hand in app.py.
- Keep an in-memory list (st.session_state.audit_trail) of every command built,
  and show it as a small table under the Device Control panel.

## Definition of done

- All tests in tests/ pass (pytest).
- core/ has no "import streamlit" anywhere. Check with grep, not just by eye.
- There is a test proving can_trigger_command(Role.TECHNICIAN) is False and
  can_trigger_command(Role.MANAGER) is True.
- There is a test proving build_command_payload raises on a bad command.
- The app runs with "streamlit run app.py" with no errors, for both a Technician
  login and a Manager login.
