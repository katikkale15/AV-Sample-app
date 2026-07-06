# 🎛️ AV Ops Dashboard — Sample App

> Built for the **Cloud and API Automation Developer** student role — NYU AV & Media Services

A tiny full-stack demo showing I can (1) pull data from two different spreadsheets into one clean UI, (2) lock features down by role (RBAC), and (3) generate the JSON payloads that would actually talk to AV hardware. No smoke and mirrors — it's ~150 lines of Python, runs in one command, and you can poke at every part of it.

🔗 **Live demo:** https://katikkale15-av-sample-app-app-59o3md.streamlit.app
📦 **Repo:** https://github.com/katikkale15/AV-Sample-app

---

## 🧠 What this actually does

| Piece | What it proves |
|---|---|
| Reads two "spreadsheets" (CSV stand-ins for Sheets A & B) | I can wire up multi-source data into one view |
| Role-based login (Technician vs. Manager) | I understand access control, not just UI |
| Manager-only "Trigger Device Command" button | I can build the control path, not just the dashboard |
| Live JSON payload on screen | This is the exact shape of thing that'd get POSTed to real AV hardware |

The whole idea: spreadsheets in, clean dashboard out, and a button that would actually *do* something in a real deployment.

---


## 🚀 Run it yourself (2 minutes)

```bash
git clone https://github.com/katikkale15/AV-Sample-app.git
cd AV-Sample-app
pip install -r requirements.txt
streamlit run app.py
```

It'll pop open at `http://localhost:8501` automatically. If it doesn't, just paste that into your browser.

---

## 🕹️ How to test both roles

1. **Log in** (sidebar) — this is a mock login standing in for real SSO, so just pick a name:
   - `Alex Chen` / `Priya Nair` → **Technician**
   - `Jordan Lee` / `Taylor Brooks` → **Manager**
2. **As Technician** → you'll see both data tables, but the control panel is hidden. There's a little warning banner confirming you're locked out of triggering anything. That's the RBAC working.
3. **As Manager** → same tables, plus a **Manager Controls** panel. Pick a device + a command, hit **Trigger Device Command**.
4. Watch the JSON payload render live underneath, e.g.:
   ```json
   {
     "command": "power_on",
     "device": "projector_1",
     "triggered_by": "Jordan Lee",
     "role": "Manager",
     "timestamp": "2026-07-06T12:34:56.000000Z"
   }
   ```
   That's the payload that would get sent via HTTP POST to a real device's control API.
5. Hit **Log out** and try the other role to compare.

---

## 📸 Adding your own screenshots

1. Run the app locally (`streamlit run app.py`)
2. Log in as a Technician, take a screenshot of the dashboard, save it as `screenshots/technician-view.png`
3. Log out, log in as a Manager, trigger a command, screenshot the JSON output, save as `screenshots/manager-view.png`
4. Create the `screenshots/` folder in your repo if it doesn't exist, drop both images in, commit and push
5. The image links above in this README will just work once those files exist in the repo

(On Mac: `Cmd+Shift+4` to screenshot a selection. On Windows: `Win+Shift+S`.)

---

## 🗂️ Files

```
av_sample_app/
├── app.py                        # the actual Streamlit app
├── av_equipment_inventory.csv    # mock Spreadsheet A
├── staff_shift_schedules.csv     # mock Spreadsheet B
├── requirements.txt
└── README.md
```

---

## ⚠️ Scope notes

This is a self-contained demo for the application's sample-app requirement — it doesn't talk to real hardware. The "device command" is simulated and rendered as JSON in the UI, exactly per the challenge instructions. Data is mock data, not real inventory or schedules.
