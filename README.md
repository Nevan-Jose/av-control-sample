# AV Operations Control Panel

A small internal tool that puts two things on one screen: the AV equipment list
and the staff shift schedule. It also controls who can do what. A Technician can
look at the data. A Manager can look at the data and also send a device command,
which creates a JSON message like a real projector or sound system would accept.

Built for the NYU AV/Media Services sample app challenge.

**Live demo:** https://av-control-sample-axddfq6ctxt4qytllhnjsr.streamlit.app
(free hosting, so if it is asleep it wakes up in a few seconds)

## What it does (and where each part lives)

| What the challenge asked for | Where it is in the code |
|---|---|
| Pull data from two sources into one screen | `core/data.py` reads `data/equipment.json` and `data/schedules.json`; `app.py` shows both tables |
| Basic security (roles) | `core/auth.py` decides what each role is allowed to do |
| Build a JSON device command | `core/payload.py` builds the command |

The two files in `data/` stand in for the two spreadsheets ("Spreadsheet A" and
"Spreadsheet B").

### Extra touches

The screen is meant to feel like a real AV panel:

- When you pick a device, it shows who is on shift in that device's room. This
  connects the two data sources instead of just showing them side by side.
- A row of quick numbers at the top: how many devices there are, how many are
  online or offline, and how many staff are on the next shift day.
- Green and red dots show which devices are online or offline.
- You can filter the tables by status, room, or shift date.
- After you send a command you can download the JSON as a file.
- A badge always shows which role you are signed in as.

## For reviewers (quick check)

Copy and paste this. It installs everything, runs the tests, and shows that the
role rules and the JSON command work, all without opening the screen:

```bash
cd av-control-sample
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1. Run the tests
pytest -q

# 2. Roles are enforced in the code, not just by hiding a button:
python -c "from core.auth import Role, can_trigger_command as c; print('Technician can trigger?', c(Role.TECHNICIAN)); print('Manager can trigger?', c(Role.MANAGER))"
#   Technician can trigger? False   /   Manager can trigger? True

# 3. The JSON command is valid and matches the example in the job post:
python -c "import json; from core.payload import build_command_payload as b; print(json.dumps(b('projector_1','power_on','Sam Patel'), indent=2))"

# 4. A bad command is rejected:
python -c "from core.payload import build_command_payload as b; b('projector_1','bogus','Sam Patel')"
#   raises ValueError

# 5. The core code has no Streamlit imports (expect no output):
grep -rn 'import streamlit' core/ || echo 'clean: core has no UI imports'
```

Then open the screen and try the two roles:

```bash
streamlit run app.py   # http://localhost:8501
```

| Sign in as | What you get |
|---|---|
| Jordan Lee (Technician) | Both tables. No device control panel. |
| Sam Patel (Manager) | Both tables plus the device control panel, where you send a command and see the JSON. |

## Setup

```bash
cd av-control-sample
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # streamlit and pytest
```

## Run the tests

```bash
pytest -v
```

The tests check role lookup, the role rules (Technician cannot send commands,
Manager can), the data loaders, the JSON command builder (right shape, and it
rejects bad commands), the helper functions, and a screen test that proves the
send button only shows for the Manager.

## Run the app

```bash
streamlit run app.py
```

It opens at http://localhost:8501.

## How to test the two roles

Sign in by picking a name from the dropdown. There is no real password (the job
post asked for basic security, not a full login system).

| Sign in as | What you see |
|---|---|
| Jordan Lee (Technician) | The top numbers, the equipment table, and the schedule table (with filters). No device control panel. |
| Sam Patel (Manager) | The same numbers and tables, plus a device control panel with device and command dropdowns, the "who is on shift in this room" note, a send button, a JSON download, and a history list. |

### Sending a device command (Manager only)

1. Sign in as Sam Patel (Manager).
2. In Device Control, pick a device (like `projector_1`) and a command (like
   `power_on`).
3. Click Trigger Device Command.
4. The JSON shows right below the button:

   ```json
   {
     "command": "power_on",
     "device": "projector_1",
     "triggered_by": "Sam Patel",
     "timestamp": "2026-06-22T14:03:11.123456+00:00"
   }
   ```

5. The history list below adds a new row for each command you send (device,
   command, who, and when). It only lasts for the current session.

The `command` and `device` keys match the example in the job post. The
`triggered_by` and `timestamp` are added so the history makes sense.

## How the role rule actually works

The device control panel only shows for a Manager. But hiding a button is not
real security on its own. So the send action checks the role again before it
builds anything. A Technician is blocked by the code, not just by a hidden
button. The check lives in one place, `can_trigger_command` in `core/auth.py`,
and both the screen and the action call it.

You can check this without the screen:

```bash
python -c "from core.auth import Role, can_trigger_command; print('TECHNICIAN:', can_trigger_command(Role.TECHNICIAN)); print('MANAGER:', can_trigger_command(Role.MANAGER))"
# TECHNICIAN: False
# MANAGER: True
```

## Project layout

```
av-control-sample/
  app.py              the screen (Streamlit, kept thin)
  requirements.txt    streamlit and pytest
  core/
    auth.py           roles and the can_trigger_command rule
    data.py           load_equipment() and load_schedules()
    payload.py        build_command_payload() and the list of valid commands
    insights.py       small helpers for the top numbers and the room match
  data/
    equipment.json    Spreadsheet A, the AV equipment list (mock)
    schedules.json    Spreadsheet B, the staff shift schedule (mock)
  tests/              test_auth, test_data, test_payload, test_insights, test_app_smoke
  .streamlit/         config.toml (a light NYU purple color)
```

All the real logic is in `core/`, and none of it imports Streamlit. That means
it can be tested on its own, without opening the screen.

