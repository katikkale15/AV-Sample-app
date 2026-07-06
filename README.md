# AV Operations Dashboard — Sample App

Built for the **Cloud and API Automation Developer** student position (AV and Media Services, NYU).

This app demonstrates:
- Pulling data from two separate spreadsheets ("AV Equipment Inventory" and "Staff Shift Schedules") into one unified UI
- Role-Based Access Control (RBAC): Technician (view-only) vs. Manager (view + trigger device command)
- JSON programming: Manager actions generate a structured JSON control payload simulating a command sent to AV hardware

## Files
- `app.py` — Streamlit application
- `av_equipment_inventory.csv` — mock Spreadsheet A
- `staff_shift_schedules.csv` — mock Spreadsheet B
- `requirements.txt` — dependencies

## Running locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to test the two roles

1. On load, you'll see a **mock login** in the sidebar (standing in for NYU SSO / real auth).
2. Select a user and click **Log in**:
   - **Alex Chen** or **Priya Nair** → logs in as **Technician**
   - **Jordan Lee** or **Taylor Brooks** → logs in as **Manager**
3. **As Technician**: you'll see both data tables (equipment + schedules) but no ability to trigger any device action — a warning message confirms the control panel is hidden.
4. **As Manager**: you'll see the same data tables, plus a **Manager Controls** panel. Select a device and a command, then click **Trigger Device Command**.
5. The generated JSON payload appears on screen immediately below the button, e.g.:
   ```json
   {
     "command": "power_on",
     "device": "projector_1",
     "triggered_by": "Jordan Lee",
     "role": "Manager",
     "timestamp": "2026-07-06T12:34:56.000000Z"
   }
   ```
   This simulates the payload that would be sent via HTTP POST to a real AV device's control API.
6. Use **Log out** in the sidebar to switch users and re-test the other role.

## Notes on scope
This is a self-contained demo built to satisfy the application's sample-app requirement. It does not contact real hardware — the "device command" is simulated and rendered as JSON in the UI, per the challenge instructions. Data is mock data, not real inventory or schedules.
