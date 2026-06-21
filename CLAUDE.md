# AV Operations Control Panel (Sample App)

> A small internal tool that puts AV Equipment Inventory and Staff Shift
> Schedules on one screen, and uses roles to decide who can just look at the
> data and who can also send a pretend device command.

This is a take-home sample app for an NYU AV/Media Services student developer
role. It is small on purpose, but built carefully: clear function shapes, tests
written first, and a clean split between data, roles, and the screen.

## 1. The idea

Right now AV operations track two things in different places: equipment status
and staff shift schedules. They should be on one screen. But not everyone who
sees that screen should be able to act on it. A Technician can see everything.
A Manager can see everything and can also send a device command, which builds a
JSON message like a real AV device (projector, audio processor, switcher) would
accept.

The exercise is meant to show three things at once:
1. Pulling two separate data sources into one screen.
2. Doing role checks the right way (in the code, not just by hiding a button).
3. Building and showing a valid JSON message for device control.

## 2. Tech choices

- Screen: Streamlit (Python). The job post lists this as an okay choice ("a
  Python-based UI like Streamlit/Gradio").
- Data: two local mock JSON files that stand in for the real Google Sheets:
  `data/equipment.json` (equipment list) and `data/schedules.json` (shift
  schedule). See [DATA.md](DATA.md).
- Tests: pytest, written first. The screen code stays thin. All the real work
  (role checks, building the JSON, loading data) lives in plain Python functions
  you can test without opening the screen.
- No real network calls. The job post says the command is only a simulation. The
  app builds the JSON and shows it on screen. It does not send it anywhere.

## 3. How it fits together

```
Screen (app.py)
    |
    |- pick a role  -> core.auth.get_role(user) -> Role
    |
    |- show Equipment + Schedule tables (both roles)
    |       |
    |       -> core.data.load_equipment() / load_schedules()
    |
    |- Manager only: Device Control panel
            |
            |- pick a device + command
            |- core.auth.can_trigger_command(role)   # role check, in code
            |- core.payload.build_command_payload(...)
            |- show the JSON + add it to the in-memory history
```

- `core/` is the logic. It has no Streamlit imports and can be tested on its own.
- The role check lives in `core.auth`, not in the screen. The screen calls
  `can_trigger_command(role)` to decide whether to show the panel, and the action
  that sends a command calls it again before doing anything. So if someone got
  past the hidden panel, a Technician is still blocked.
- The history is a simple in-memory list of every command sent (who, what,
  when), shown at the bottom of the Manager view.

## 4. Folder layout

```
/
  CLAUDE.md         this file
  DATA.md           the mock data and roles
  CONTRACTS.md      the function shapes (do not change them on a whim)
  build.md          the build steps
  run.md            how to run and test
  app.py            the screen (Streamlit, thin)
  core/
    __init__.py
    auth.py         Role, ROLE_PERMISSIONS, can_trigger_command()
    data.py         load_equipment(), load_schedules()
    payload.py      build_command_payload()
    insights.py     small helpers for the top numbers and the room match
  data/
    equipment.json
    schedules.json
  tests/
    test_auth.py
    test_data.py
    test_payload.py
    test_insights.py
    test_app_smoke.py
  README.md         what to submit and how to test the roles
```

## 5. Build plan

### Phase 0: core logic, tests first
- `core.auth`: Role enum (TECHNICIAN, MANAGER) and can_trigger_command(role).
- `core.data`: loaders for the two JSON files.
- `core.payload`: build_command_payload(device, command, triggered_by), matching
  the shape in [CONTRACTS.md](CONTRACTS.md).
- All three pass their tests before any screen code is written.

### Phase 1: the screen
- A role picker to sign in.
- One screen with both tables (equipment and schedule), shown to both roles.
- A Manager-only Device Control panel: a device dropdown (filled from the data,
  not hardcoded), a command dropdown, and a send button.
- On send: build the JSON with `core.payload`, show it, and add it to the
  in-memory history table.
- A README that explains how to test both roles.

There is no Phase 2. This is a small, finished piece of work. Do not add extra
scope (real hardware, a database, real login) beyond what is here unless asked.

## 6. Rules for anyone working on this

- `core/` must have no Streamlit imports. If a function needs to import
  streamlit, it belongs in app.py, not core/.
- Every function in [CONTRACTS.md](CONTRACTS.md) is fixed once its tests pass. Do
  not change its shape later without updating CONTRACTS.md first.
- Check the role at the moment of the action (inside the function that does the
  real thing), not only when drawing a button.
- Read [DATA.md](DATA.md) before writing the loaders or the data. Do not add
  fields that are not listed there.
