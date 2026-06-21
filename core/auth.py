"""Roles and the rule for who can send a device command.

This file is the one place that decides what a role can do. The screen uses
can_trigger_command to decide whether to show the Device Control panel, and the
action that sends a command calls it again before doing anything. So the rule is
in the code, not just hidden in the screen.

There are no Streamlit imports here, so this stays plain and easy to test.
"""
from enum import Enum


class Role(str, Enum):
    TECHNICIAN = "TECHNICIAN"
    MANAGER = "MANAGER"


# Login table: the name you pick at sign in maps to a role. No real password.
USERS: dict[str, Role] = {
    "Jordan Lee": Role.TECHNICIAN,
    "Sam Patel": Role.MANAGER,
}

# What each role can do. Kept as a tiny dict on purpose, not a big permissions
# system. Right now the only thing to allow or block is sending a command.
ROLE_PERMISSIONS: dict[Role, dict[str, bool]] = {
    Role.TECHNICIAN: {"trigger_command": False},
    Role.MANAGER: {"trigger_command": True},
}


def get_role(user_name: str) -> Role | None:
    """Find the role for a user name. Returns None if it is not recognized."""
    return USERS.get(user_name)


def can_trigger_command(role: Role) -> bool:
    """True only for Manager. This is the one rule for who can send a command.
    The screen and the action both call this instead of repeating the check."""
    return ROLE_PERMISSIONS.get(role, {}).get("trigger_command", False)
