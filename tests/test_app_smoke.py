"""Screen test using Streamlit's AppTest.

Most logic is tested directly in core/ (no screen needed). This one test checks
the whole screen: it proves the role rule reaches the screen, so the Device
Control button shows up only for the Manager. It backs up the check in
test_auth.py.
"""
from streamlit.testing.v1 import AppTest


def _run_as(user: str) -> AppTest:
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value(user).run()  # login selectbox
    at.button[0].click().run()             # "Sign in"
    return at


def test_manager_sees_device_control_trigger():
    at = _run_as("Sam Patel")
    assert not at.exception
    assert any("Trigger Device Command" in b.label for b in at.button)


def test_technician_cannot_see_device_control_trigger():
    at = _run_as("Jordan Lee")
    assert not at.exception
    assert not any("Trigger Device Command" in b.label for b in at.button)


def test_both_roles_see_both_data_tables():
    for user in ("Sam Patel", "Jordan Lee"):
        at = _run_as(user)
        assert not at.exception
        # Equipment + Schedule tables render for everyone.
        assert len(at.dataframe) >= 2
