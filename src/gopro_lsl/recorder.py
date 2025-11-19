"""
High-level recording orchestration.
Coordinates GoPro recording with LSL markers.
"""

import time
from .gopro_control import start_recording, stop_recording
from .lsl_marker_stream import send_marker

def record_session(duration_sec: int, marker_start: str = "START", marker_stop: str = "STOP"):
    """
    Record a session on GoPro and send LSL markers.
    
    Args:
        duration_sec (int): Duration to record in seconds.
        marker (str): Marker label to push at start.
    """
    print("Starting recording session...")
    send_marker(marker_start)   # Push start marker
    start_recording()
    try:
        time.sleep(duration_sec)
    except KeyboardInterrupt:
        print("Recording interrupted!")
    stop_recording()
    send_marker("END")
    print("Recording session completed")
    send_marker(marker_end)   # Push end marker