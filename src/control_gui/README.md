# Control GUI

A desktop control panel for the scripts in `src/scripts/`. It gives each one a
tab with Start/Stop, live console output, and a status badge, instead of
having to open several terminals.

## Run it

From the project root:

```bash
python -m src.scripts.start_gui
```

Requires Python 3.10+ with `tkinter` (bundled with the standard CPython
installer on Windows/macOS; on Linux install `python3-tk` if it's missing).

## Environment bar

The bar at the top of the window picks which Python interpreter is used to
launch every tab's script (`python -m ...`). It:

- auto-detects a `venv`/`.venv`/`env` folder in the project root, plus the
  system `python` and the interpreter currently running the GUI
- lets you `Browse...` to any other `python.exe`
- validates the selection by running `<path> --version` and shows the result
- remembers your choice in `.gui_config.json` (project root, git-ignored) so
  it's picked up again next launch

Pick an interpreter that has this project's `requirements.txt` installed
(plus the Rebocap SDK's dependencies if you'll use that tab).

## Tabs

**MQTT control** — runs `send_mqtt_broadcast_start` / `send_mqtt_broadcast_stop`
as one-shot commands. Since agents don't send an acknowledgement back, click
again if you're not sure it landed — every attempt and its exit code is kept
in the history list below so you can see what was actually sent and when.

**Motion agent** — runs `start_motion_agent` (`src.scripts.start_motion_agent`).
Start/Terminate it like any long-running process; output streams live into
the console.

**GoPro / RPi** — runs `start_rpi_agent_with_heartbeat`, same Start/Terminate
+ live console pattern as Motion agent.

**Rebocap test** — runs `lib/rebocap_python_sdk_v2/rebocap_ws_sdk_example.py`
directly, independent of the other tabs. This connects to the **Rebocap
desktop app's** local websocket server on port 7690 — it does not talk to the
suit directly. If you see:

```
[fail] WebSocket Connection Unknown - "" / 0 websocketpp.transport:9 Timer Expired
[error] handle_connect error: Timer Expired
```

it means nothing is listening on port 7690 — start the Rebocap desktop app
(with the suit connected/calibrated) before clicking Start here.

## Console output

Every console is read-only but fully copyable: drag-select and `Ctrl+C`, or
right-click for Copy / Select all / Clear. Lines are colored by content
(errors in red, warnings in amber, connected/success/heartbeat lines in
green) to make scanning long output easier.

## Troubleshooting

- **MQTT tab shows a non-zero exit / "Error publishing MQTT message"** — no
  broker reachable at the address in `src/mqtt_commander/config.py`. Confirm
  mosquitto (or your broker) is running and the `MQTT_BROKER` host is correct.
- **Environment badge shows "invalid"** — the selected path isn't a working
  Python executable; browse to a real `python.exe`.
- **A tab's console shows LSL/websocket connection errors after Start** —
  this usually means a script tried to reach real hardware (Rebocap suit/app,
  GoPro, RPi) that isn't connected yet, not a bug in the GUI itself.
