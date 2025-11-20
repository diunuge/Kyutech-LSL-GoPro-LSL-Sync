"""
Recorder module for GoPro + LSL integration.
Handles starting/stopping GoPro recordings and sending LSL markers.
"""

import time
from src.gopro_lsl.gopro_control import start_recording, stop_recording
from src.gopro_lsl.lsl_marker_stream import MarkerSender
from src.gopro_lsl.config import MARKER_START, MARKER_STOP

# Global marker sender instance
marker_sender = MarkerSender()
recording_active = False


def start_record_session():
    """Start a recording session with GoPro and LSL markers."""
    global recording_active
    if recording_active:
        print("[Recorder] Recording already active.")
        return

    print("[Recorder] Starting GoPro + LSL session...")

    
    status = start_recording() # Start GoPro recording
    if status:
        marker_sender.send_marker(MARKER_START) # Send START marker
        marker_sender.start_heartbeat() # Start LSL heartbeat in background
        recording_active = True
    else:
        return


def stop_record_session():
    """Stop the recording session."""
    global recording_active
    if not recording_active:
        print("[Recorder] No active recording.")
        return

    print("[Recorder] Stopping GoPro + LSL session...")
    
    marker_sender.send_marker(MARKER_STOP) # Push STOP marker
    stop_recording() # Stop GoPro recording
    marker_sender.stop_heartbeat() # Push LSL heartbeat

    recording_active = False


def record_session(duration_sec: int, marker_start: str = "START", marker_stop: str = "STOP"):
    """
    Record a session on GoPro and send LSL markers.
    
    Args:
        duration_sec (int): Duration to record in seconds.
        marker (str): Marker label to push at start.
    """
    print("Starting recording session...")
    marker_sender.send_marker(marker_start)   # Push start marker
    start_recording()
    try:
        time.sleep(duration_sec)
    except KeyboardInterrupt:
        print("Recording interrupted!")
    stop_recording()
    marker_sender.send_marker(marker_stop)   # Push end marker
    print("Recording session completed")


