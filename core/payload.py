"""Builds the JSON command that pretends to control an AV device.

This is the "JSON for device control" part of the challenge. It builds the
message and hands it back. It does not send it anywhere, because the job post
says the command is only a simulation.

This file does not check roles. That is the job of core.auth, and app.py calls
can_trigger_command before it ever calls this. No Streamlit imports here.
"""
from datetime import datetime, timezone

VALID_COMMANDS = {"power_on", "power_off", "input_select", "mute"}


def build_command_payload(
    device_id: str,
    command: str,
    triggered_by: str,
) -> dict:
    """Build the JSON command. Raises ValueError if the command is not in
    VALID_COMMANDS.

    Returns exactly:
    {
        "command": <command>,
        "device": <device_id>,
        "triggered_by": <triggered_by>,
        "timestamp": <ISO 8601 string, UTC>
    }
    """
    if command not in VALID_COMMANDS:
        raise ValueError(
            f"Invalid command {command!r}. Valid commands: {sorted(VALID_COMMANDS)}"
        )

    return {
        "command": command,
        "device": device_id,
        "triggered_by": triggered_by,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
