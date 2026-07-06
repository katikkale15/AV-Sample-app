import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="AV Ops Dashboard - Sample App", layout="wide")

# ---------------------------------------------------------------------------
# Mock user directory (login = username, in a real system this would be
# NYU SSO / a proper auth provider). Two roles: Technician, Manager.
# ---------------------------------------------------------------------------
USERS = {
    "alex.chen": {"name": "Alex Chen", "role": "Technician"},
    "priya.nair": {"name": "Priya Nair", "role": "Technician"},
    "jordan.lee": {"name": "Jordan Lee", "role": "Manager"},
    "taylor.brooks": {"name": "Taylor Brooks", "role": "Manager"},
}

DEVICE_COMMANDS = {
    "power_on": "Power On",
    "power_off": "Power Off",
    "mute": "Mute Audio",
    "input_hdmi1": "Switch Input to HDMI 1",
}

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "command_log" not in st.session_state:
    st.session_state.command_log = []

# ---------------------------------------------------------------------------
# Sidebar: login
# ---------------------------------------------------------------------------
st.sidebar.title("🔐 Login")

if st.session_state.logged_in_user is None:
    username = st.sidebar.selectbox(
        "Select user (mock SSO)",
        options=list(USERS.keys()),
        format_func=lambda u: f"{USERS[u]['name']} ({USERS[u]['role']})",
    )
    if st.sidebar.button("Log in"):
        st.session_state.logged_in_user = username
        st.rerun()
    st.info("👈 Select a mock user in the sidebar and click **Log in** to view the dashboard.")
    st.stop()
else:
    user = USERS[st.session_state.logged_in_user]
    st.sidebar.success(f"Logged in as **{user['name']}**\n\nRole: **{user['role']}**")
    if st.sidebar.button("Log out"):
        st.session_state.logged_in_user = None
        st.rerun()

role = user["role"]

st.title("AV Operations Dashboard")
st.caption("Sample application — unified view of AV equipment inventory and staff shift schedules, with role-based access control (RBAC).")

# ---------------------------------------------------------------------------
# Load mock data (Spreadsheet A + Spreadsheet B)
# ---------------------------------------------------------------------------
equipment_df = pd.read_csv("av_equipment_inventory.csv")
schedule_df = pd.read_csv("staff_shift_schedules.csv")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Spreadsheet A — AV Equipment Inventory")
    st.dataframe(equipment_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🗓️ Spreadsheet B — Staff Shift Schedules")
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)

st.divider()

# ---------------------------------------------------------------------------
# Role-gated section
# ---------------------------------------------------------------------------
if role == "Technician":
    st.subheader("🔧 Technician View")
    st.write(
        "You have **view-only** access. Technicians can see equipment and schedule "
        "data above, but cannot trigger device commands."
    )
    st.warning("Trigger Device Command button is hidden for the Technician role.")

elif role == "Manager":
    st.subheader("🛠️ Manager Controls")
    st.write("You have **view + control** access. Use the panel below to trigger a device command.")

    with st.form("device_command_form"):
        device_id = st.selectbox("Select device", equipment_df["equipment_id"].tolist())
        command = st.selectbox(
            "Select command",
            options=list(DEVICE_COMMANDS.keys()),
            format_func=lambda c: DEVICE_COMMANDS[c],
        )
        submitted = st.form_submit_button("🚀 Trigger Device Command")

    if submitted:
        payload = {
            "command": command,
            "device": device_id,
            "triggered_by": user["name"],
            "role": role,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        st.session_state.command_log.insert(0, payload)
        st.success("Command payload generated and (simulated) sent to device.")

    if st.session_state.command_log:
        st.markdown("#### Generated JSON control payload (most recent first)")
        for i, payload in enumerate(st.session_state.command_log):
            st.code(json.dumps(payload, indent=2), language="json")
            if i == 0:
                st.caption("⬆️ Most recent command — this is the JSON payload that would be POSTed to the device's control API.")

st.divider()
st.caption(
    "Note: this is a self-contained demo. Device commands are simulated (printed as JSON), "
    "no real hardware is contacted. Data is mock/sample data for demonstration purposes only."
)
