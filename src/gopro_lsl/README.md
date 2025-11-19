# GoPro + LSL Integration Module (`gopro_lsl`)

This folder contains all modules required for controlling a GoPro camera over Wi-Fi and synchronizing experimental events using LabStreamingLayer (LSL). It forms the core component for experiments where a GoPro recording must be aligned with timestamps or other devices.

## Overview

The package provides the following functionality:
- Start and stop GoPro recording using its HTTP API.
- Create an LSL marker stream for synchronized timestamps.
- Send individual markers or periodic time-aligned markers.
- Run a complete recording session with precise timing (start, markers, stop).
- Centralized configuration for GoPro IP, default durations, and marker frequency.

## Folder Contents

src/gopro_lsl/
 ├── __init__.py
 ├── gopro_control.py
 ├── lsl_marker_stream.py
 ├── recorder.py
 └── config.py

## Installation Requirements

Install dependencies manually:
```
pip install pylsl requests
```

Or install the project requirements:
```
pip install -r requirements.txt
```

## Configuration (`config.py`)
Configure following:

```
GOPRO_IP = "10.5.5.9"
DEFAULT_RECORDING_DURATION = 60
HEARTBEAT_HZ = 1.0
```

## Usage

### Start and stop recording
```
from src.gopro_lsl.gopro_control import shutter
shutter(True)
shutter(False)
```

### Send LSL markers
```
from src.gopro_lsl.lsl_marker_stream import create_marker_stream, send_marker
outlet = create_marker_stream()
send_marker(outlet, "SYNC_001")
```

### Full recording session
```
from src.gopro_lsl.recorder import record_session
record_session(duration_sec=20, marker="EXP_START")
```

## Running From Script

```
python -m src.scripts.run_gopro_recording
```

Custom:
```
python -m src.scripts.run_gopro_recording --duration 30 --marker SYNC
```

## Troubleshooting
- Ensure GoPro Wi-Fi connection.
- Verify IP via: http://10.5.5.9/gp/gpControl/status
- Disable VPN/firewall if LSL not visible.
- Always run using module mode.
