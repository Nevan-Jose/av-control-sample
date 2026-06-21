# run.md: Run, Test, and Submit

How to run the AV Operations Control Panel sample app. For the plan see
[CLAUDE.md](CLAUDE.md), for the data see [DATA.md](DATA.md), for the function
shapes see [CONTRACTS.md](CONTRACTS.md), and for the build steps see
[build.md](build.md).

## 1. Setup

```bash
cd av-control-sample
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install streamlit pytest
```

## 2. Run the tests

```bash
pytest -v
```

All tests should pass before you run the app.

## 3. Run the app

```bash
streamlit run app.py
```

Opens at http://localhost:8501.

## 4. How to test both roles

| Sign in as | Role | What you should see |
|----------|------|----------------------|
| Jordan Lee | Technician | Equipment table and Staff Shift Schedule table. No Device Control panel. |
| Sam Patel | Manager | The same two tables, plus a Device Control panel with device and command dropdowns and a "Trigger Device Command" button. |

To test the command flow as Manager:
1. Pick a device (like projector_1) and a command (like power_on).
2. Click Trigger Device Command.
3. The JSON shows on screen, like:
   ```json
   {
     "command": "power_on",
     "device": "projector_1",
     "triggered_by": "Sam Patel",
     "timestamp": "2026-06-22T14:03:11.123456+00:00"
   }
   ```
4. Scroll down to the history table. The command you just sent shows up as a new
   row.

## 5. What is left out on purpose

From CLAUDE.md's plan: no real login (the job post asks for basic security, not a
full login system), no real network call to AV hardware (the post says the
command is simulated), and no database (an in-memory history is enough for a
take-home sample).

## 6. Submitting

From the job post's Application Requirements, package this up:
- The whole project folder (zip it, or push it to a repo and share the link).
- Make sure data/equipment.json and data/schedules.json are included as the mock
  data sources.
- README.md is the short instructions the post asks for: how to test the roles,
  how the command is sent, and where the JSON shows up.
