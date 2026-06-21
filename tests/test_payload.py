"""Tests for core.payload: the builder for the JSON device command.

Per CONTRACTS.md: build_command_payload returns exactly
{command, device, triggered_by, timestamp}; raises ValueError on a bad command;
timestamp is an ISO 8601 UTC string. Checking roles is not this file's job.
"""
from datetime import datetime, timezone

import pytest

from core.payload import VALID_COMMANDS, build_command_payload


def test_valid_commands_set():
    assert VALID_COMMANDS == {"power_on", "power_off", "input_select", "mute"}


def test_valid_command_builds_exact_shape():
    payload = build_command_payload("projector_1", "power_on", "Sam Patel")
    assert set(payload.keys()) == {"command", "device", "triggered_by", "timestamp"}
    assert payload["command"] == "power_on"
    assert payload["device"] == "projector_1"
    assert payload["triggered_by"] == "Sam Patel"


def test_matches_job_posting_example_keys():
    # Job posting example: {"command": "power_on", "device": "projector_1"}
    payload = build_command_payload("projector_1", "power_on", "Sam Patel")
    assert payload["command"] == "power_on"
    assert payload["device"] == "projector_1"


def test_invalid_command_raises_value_error():
    with pytest.raises(ValueError):
        build_command_payload("projector_1", "self_destruct", "Sam Patel")


def test_timestamp_is_iso8601_utc():
    payload = build_command_payload("projector_1", "mute", "Sam Patel")
    parsed = datetime.fromisoformat(payload["timestamp"])
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == timezone.utc.utcoffset(None)


@pytest.mark.parametrize("command", sorted(VALID_COMMANDS))
def test_every_valid_command_is_accepted(command):
    payload = build_command_payload("dsp_main_hall", command, "Sam Patel")
    assert payload["command"] == command
