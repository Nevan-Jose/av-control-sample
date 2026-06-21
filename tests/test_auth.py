"""Tests for core.auth: role lookup and the rule for sending commands.

Per CONTRACTS.md: Role enum (TECHNICIAN, MANAGER), USERS dict, get_role(),
and can_trigger_command(), which is the one place the rule lives.
"""
from core.auth import Role, USERS, get_role, can_trigger_command


def test_role_is_str_enum_with_two_members():
    assert Role.TECHNICIAN.value == "TECHNICIAN"
    assert Role.MANAGER.value == "MANAGER"
    assert {r for r in Role} == {Role.TECHNICIAN, Role.MANAGER}


def test_known_user_resolves_to_correct_role():
    assert get_role("Jordan Lee") == Role.TECHNICIAN
    assert get_role("Sam Patel") == Role.MANAGER


def test_unknown_user_returns_none():
    assert get_role("Nobody McNobody") is None


def test_users_dict_matches_data_md():
    assert USERS == {
        "Jordan Lee": Role.TECHNICIAN,
        "Sam Patel": Role.MANAGER,
    }


def test_can_trigger_command_true_only_for_manager():
    assert can_trigger_command(Role.MANAGER) is True
    assert can_trigger_command(Role.TECHNICIAN) is False
