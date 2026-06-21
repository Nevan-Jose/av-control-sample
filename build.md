# build.md: Build Steps (tests first)

How to build this app, tests first. This is a single sitting. The app is small,
so there is nothing to split up.

Read [CLAUDE.md](CLAUDE.md) for the plan, [DATA.md](DATA.md) for the exact data,
and [CONTRACTS.md](CONTRACTS.md) for the function shapes before writing any code.

## 0. Main ideas (read once)

1. Tests first, always. For every function: write a failing test, run it to see
   it fail, write the smallest code to make it pass, then clean up. No code
   before there is a failing test for it.
2. Function shapes are fixed once their tests pass. If a later step seems to need
   a change, stop and re-read CONTRACTS.md first.
3. core/ has no screen imports. The logic can be tested without Streamlit. If you
   want to import streamlit inside core/, that code belongs in app.py.
4. Role checks live in the code, not just in the screen. A test must prove that
   can_trigger_command returns False for TECHNICIAN. A hidden button is not
   enough on its own.
5. Done means: all tests pass, core/ has no Streamlit imports, the app runs with
   no errors for both roles, and the README explains how to test both roles.

## 1. One-time setup

```bash
mkdir -p av-control-sample && cd av-control-sample
python3 -m venv .venv && source .venv/bin/activate
pip install streamlit pytest
```

Files to create (see CLAUDE.md section 4 for the full layout):

```
core/__init__.py
core/auth.py
core/data.py
core/payload.py
data/equipment.json
data/schedules.json
tests/test_auth.py
tests/test_data.py
tests/test_payload.py
app.py
README.md
```

## 2. Build order (one sitting, in order)

This is the prompt to paste into Claude Code, in one go:

```
Read CLAUDE.md, DATA.md, and CONTRACTS.md fully before doing anything.

Use strict tests-first. For every function: write a failing test, run it to see
it fail, write the smallest code to pass, then clean up. Never write code before
a failing test exists for it.

Build in this order:

1. data/equipment.json and data/schedules.json. Use the exact mock rows from
   DATA.md sections 2 and 3.

2. core/auth.py, tests first. Build the Role enum, USERS dict, get_role, and
   can_trigger_command exactly as in CONTRACTS.md. Write tests proving: a known
   login resolves to the right role, an unknown one returns None, and
   can_trigger_command is True only for MANAGER.

3. core/data.py, tests first. Build load_equipment and load_schedules. Write
   tests proving each returns a list of dicts with the exact fields from
   DATA.md, loaded from the JSON files.

4. core/payload.py, tests first. Build build_command_payload exactly as in
   CONTRACTS.md, including VALID_COMMANDS. Write tests proving: a valid command
   builds the exact shape, a bad command raises ValueError, and the timestamp is
   a valid ISO 8601 string.

5. Only after all of the above pass: app.py. A Streamlit app that:
   - Has a sign-in (a dropdown from core.auth.USERS keys).
   - On sign-in, finds the role with core.auth.get_role.
   - Shows the Equipment and Schedule tables (via core.data) for both roles,
     using st.dataframe or st.table.
   - If core.auth.can_trigger_command(role) is True, shows a Device Control
     panel: a device dropdown filled from the loaded data (not hardcoded), a
     command dropdown limited to core.payload.VALID_COMMANDS, and a "Trigger
     Device Command" button.
   - On click, calls core.payload.build_command_payload, shows the JSON, and adds
     it to st.session_state.audit_trail, which is shown as a small table below
     (columns: device, command, triggered_by, timestamp).
   - Does not show the Device Control panel for TECHNICIAN. Remember the real
     block is the can_trigger_command check; hiding the panel is just on top of
     that.

6. README.md. How to install, run the app, and test both roles (which role to
   pick, what each role can and cannot do, where the JSON shows up, and where the
   history shows up).

Done means: all tests pass, core/ has no "import streamlit" (check with grep),
and the app runs with "streamlit run app.py" with no errors for both Jordan Lee
(Technician) and Sam Patel (Manager).
```

## 3. Checklist (keep this in view)

- [ ] Failing test first, always. If you catch yourself writing code before a
      failing test exists, stop, delete it, and start that step with the test.
- [ ] No extra scope. No real login, no database, no real network call. None of
      that is in the plan, and the job post says the command is simulated.
- [ ] Shapes stay fixed. If CONTRACTS.md needs to change, change the doc first,
      then the code. Never let them drift apart.
- [ ] Check the split before calling it done: grep -r "import streamlit" core/
      should return nothing.
- [ ] Test both roles by hand before submitting. Sign in as Jordan Lee
      (Technician) and check the Device Control panel is really gone. Sign in as
      Sam Patel (Manager) and send a real command from start to finish.
