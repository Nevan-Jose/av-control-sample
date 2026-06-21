"""AV Operations Control Panel: the screen (Streamlit).

This file only handles the screen. All the real work (roles, data, JSON) is in
core/. The screen never does role lookup on its own, never builds the JSON by
hand, and only shows the Device Control panel when core.auth says the role is
allowed.
"""
import json

import streamlit as st

from core.auth import USERS, Role, can_trigger_command, get_role
from core.data import load_equipment, load_schedules
from core.insights import equipment_summary, staff_for_location, staff_on_date
from core.payload import VALID_COMMANDS, build_command_payload

STATUS_ICON = {"online": "🟢", "offline": "🔴"}


def trigger_device_command(
    role: Role, device_id: str, command: str, triggered_by: str
) -> dict:
    """Send a device command.

    The role is checked again right here, at the moment of the action. So even
    if someone got past the hidden panel, a Technician still cannot build a
    command. This is the real block, not just a hidden button.
    """
    if not can_trigger_command(role):
        raise PermissionError(
            f"Role {role.value} is not allowed to send device commands."
        )
    return build_command_payload(device_id, command, triggered_by)


def _decorate_equipment(rows: list[dict]) -> list[dict]:
    """Add a colored dot to the status so it is easy to scan."""
    return [
        {**r, "status": f"{STATUS_ICON.get(r['status'], '')} {r['status']}".strip()}
        for r in rows
    ]


def render_login() -> None:
    """Pick a name to sign in. There is no real password (per DATA.md)."""
    st.subheader("Sign in")
    st.caption("Pick a name to sign in. There is no real password.")
    name = st.selectbox("Sign in as", options=list(USERS.keys()), index=None,
                        placeholder="Select a user...")
    if st.button("Sign in", type="primary", disabled=name is None):
        st.session_state.user = name
        st.rerun()


def render_summary(equipment: list[dict], schedules: list[dict]) -> None:
    """A row of quick numbers at the top, taken from both data files."""
    summary = equipment_summary(equipment)
    next_date = min((s["shift_date"] for s in schedules), default=None)
    on_next = staff_on_date(schedules, next_date) if next_date else []

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Devices", summary["total"])
    c2.metric("🟢 Online", summary["online"])
    c3.metric("🔴 Offline", summary["offline"])
    c4.metric(f"On shift {next_date or 'n/a'}", len(on_next))


def render_data_tables(equipment: list[dict], schedules: list[dict]) -> None:
    """The two tables. Both roles can see these. Each one has a simple filter."""
    st.subheader("AV Equipment Inventory")
    st.caption("Spreadsheet A")
    statuses = ["All"] + sorted({e["status"] for e in equipment})
    rooms = ["All"] + sorted({e["room"] for e in equipment})
    fc1, fc2 = st.columns(2)
    status_f = fc1.selectbox("Filter by status", statuses)
    room_f = fc2.selectbox("Filter by room", rooms, key="eq_room")
    eq_view = [
        e for e in equipment
        if (status_f == "All" or e["status"] == status_f)
        and (room_f == "All" or e["room"] == room_f)
    ]
    st.dataframe(_decorate_equipment(eq_view), width="stretch", hide_index=True)

    st.subheader("Staff Shift Schedule")
    st.caption("Spreadsheet B")
    dates = ["All"] + sorted({s["shift_date"] for s in schedules})
    date_f = st.selectbox("Filter by shift date", dates)
    sch_view = [s for s in schedules if date_f == "All" or s["shift_date"] == date_f]
    st.dataframe(sch_view, width="stretch", hide_index=True)


def render_device_control(user: str, role: Role, equipment: list[dict],
                          schedules: list[dict]) -> None:
    """The Device Control panel. Only shown when the role is allowed."""
    st.subheader("Device Control")
    st.caption("Manager only. Builds a JSON command (this is a simulation).")

    by_id = {row["device_id"]: row for row in equipment}
    device_ids = list(by_id)
    labels = {d: f"{by_id[d]['name']} ({d})" for d in device_ids}

    col1, col2 = st.columns(2)
    with col1:
        device_id = st.selectbox("Device", options=device_ids,
                                 format_func=lambda d: labels[d])
    with col2:
        command = st.selectbox("Command", options=sorted(VALID_COMMANDS))

    # Show who is on shift in the room this device is in.
    device = by_id[device_id]
    on_shift = staff_for_location(schedules, device["room"])
    status_label = f"{STATUS_ICON.get(device['status'], '')} {device['status']}"
    st.caption(f"📍 {device['room']} · status {status_label}")
    if on_shift:
        names = ", ".join(f"{s['staff_name']} ({s['time_block']}, {s['shift_date']})"
                          for s in on_shift)
        st.info(f"👤 On shift in this room: {names}")
    else:
        st.warning("⚠️ No staff scheduled in this room.")

    if st.button("Trigger Device Command", type="primary"):
        try:
            payload = trigger_device_command(role, device_id, command, user)
        except PermissionError as exc:
            st.error(str(exc))
        else:
            st.session_state.audit_trail.append(payload)
            st.success("Command created (simulated, not sent anywhere).")
            st.json(payload)
            st.download_button(
                "⬇️ Download payload (.json)",
                data=json.dumps(payload, indent=2),
                file_name=f"command_{payload['device']}_{payload['command']}.json",
                mime="application/json",
            )

    if st.session_state.audit_trail:
        st.markdown("**Command history** (this session only)")
        st.dataframe(
            st.session_state.audit_trail,
            width="stretch",
            hide_index=True,
            column_order=("device", "command", "triggered_by", "timestamp"),
        )


def render_role_badge(user: str, role: Role) -> None:
    """Show who is signed in and what they can do."""
    if role == Role.MANAGER:
        st.success(f"👤 Signed in as {user} (Manager). Full access (can send commands).")
    else:
        label = role.value.title() if role else "Unknown"
        st.info(f"👤 Signed in as {user} ({label}). View only.")


def main() -> None:
    st.set_page_config(page_title="AV Operations Control Panel", page_icon="🎛️",
                       layout="wide")
    st.title("🎛️ AV Operations Control Panel")
    st.caption("AV equipment and staff schedules on one screen, with device control by role.")

    st.session_state.setdefault("user", None)
    st.session_state.setdefault("audit_trail", [])

    if st.session_state.user is None:
        render_login()
        return

    user = st.session_state.user
    role = get_role(user)
    equipment = load_equipment()
    schedules = load_schedules()

    with st.sidebar:
        st.markdown(f"**User:** {user}")
        st.markdown(f"**Role:** {role.value if role else 'UNKNOWN'}")
        if st.button("Sign out"):
            st.session_state.user = None
            st.rerun()

    render_role_badge(user, role)
    render_summary(equipment, schedules)
    st.divider()
    render_data_tables(equipment, schedules)

    # Show the Device Control panel only if the role is allowed to use it.
    if role is not None and can_trigger_command(role):
        st.divider()
        render_device_control(user, role, equipment, schedules)
    else:
        st.info("View only. Device Control is for Managers.")


if __name__ == "__main__":
    main()
