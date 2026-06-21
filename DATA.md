# DATA: Mock Data and Roles

This is the reference for the two mock data sources and the roles. Use these
exact fields when building `core/data.py` and the JSON files in `data/`. Do not
add fields that are not listed here.

These stand in for "Spreadsheet A" (AV Equipment Inventory) and "Spreadsheet B"
(Staff Shift Schedules) from the job post.

## 1. Roles

Two roles only:

| Role | Can view Equipment + Schedules | Can send device command |
|------|:---:|:---:|
| TECHNICIAN | yes | no |
| MANAGER | yes | yes |

No other roles and no extra permission levels. Keep `core.auth` simple: a small
dict from role to what it can do, not a big permissions system.

Login is just picking a name (no real password, which matches the job post's
"basic security"). Suggested mock users:

| Name | Role |
|------|------|
| Jordan Lee | TECHNICIAN |
| Sam Patel | MANAGER |

## 2. Spreadsheet A: AV Equipment Inventory

Fields per row:

| Field | Type | Example |
|-------|------|---------|
| device_id | string | projector_1 |
| name | string | Epson Pro L730U |
| type | string | projector, dsp, switcher, or display |
| room | string | Dibner Hall 101 |
| status | string | online or offline |
| last_serviced | date string (YYYY-MM-DD) | 2026-04-12 |

Mock rows (realistic device and room names, NYU Tandon flavor is fine):

```json
[
  {"device_id": "projector_1", "name": "Epson Pro L730U", "type": "projector", "room": "Dibner Hall 101", "status": "online", "last_serviced": "2026-04-12"},
  {"device_id": "dsp_main_hall", "name": "QSC Core 110f", "type": "dsp", "room": "Jacobs Lecture Hall", "status": "online", "last_serviced": "2026-03-02"},
  {"device_id": "switcher_2", "name": "Extron DTP CrossPoint 84", "type": "switcher", "room": "6 MetroTech 201", "status": "offline", "last_serviced": "2026-01-20"},
  {"device_id": "display_3", "name": "Samsung QM85R", "type": "display", "room": "370 Jay St Conf Room A", "status": "online", "last_serviced": "2026-05-30"}
]
```

The device_id values are the IDs used in the Device Control dropdown and in the
JSON command. Keep them stable.

## 3. Spreadsheet B: Staff Shift Schedules

Fields per row:

| Field | Type | Example |
|-------|------|---------|
| staff_name | string | Jordan Lee |
| role | string | Technician or Manager |
| shift_date | date string (YYYY-MM-DD) | 2026-06-22 |
| time_block | string | 09:00-13:00 |
| assigned_location | string | Dibner Hall 101 |

Mock rows:

```json
[
  {"staff_name": "Jordan Lee", "role": "Technician", "shift_date": "2026-06-22", "time_block": "09:00-13:00", "assigned_location": "Dibner Hall 101"},
  {"staff_name": "Sam Patel", "role": "Manager", "shift_date": "2026-06-22", "time_block": "12:00-20:00", "assigned_location": "Jacobs Lecture Hall"},
  {"staff_name": "Priya Nair", "role": "Technician", "shift_date": "2026-06-23", "time_block": "13:00-21:00", "assigned_location": "6 MetroTech 201"}
]
```

## 4. Device commands

The Device Control panel has a small, fixed set of commands. Enough to be
realistic without overdoing it:

| Command | Meaning |
|---------|---------|
| power_on | Turn the device on |
| power_off | Turn the device off |
| input_select | Switch the input source |
| mute | Mute the audio |

These are the only valid values for the command field. See [CONTRACTS.md](CONTRACTS.md).
