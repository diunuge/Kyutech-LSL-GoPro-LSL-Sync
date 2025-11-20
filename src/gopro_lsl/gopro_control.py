"""
GoPro control module.
Provides functions to start and stop recording and query camera status.
"""

import requests
from datetime import datetime
from src.gopro_lsl.config import GOPRO_IP

def log(msg):
    print(f"[{datetime.now().strftime("%H:%M:%S.%f")[:-3]}] {msg}")

def start_recording(timeout=5.0, poll_interval=0.2):
    """
    Send start-recording command to GoPro and confirm encoding has started.
    
    Returns:
        True  → recording successfully started
        False → failed or timed out
    """
    try:
        # Send shutter start command
        url = f"http://{GOPRO_IP}/gp/gpControl/command/shutter?p=1"
        response = requests.get(url, timeout=2)
        log("Start command sent")
        if response.status_code != 200:
            print("Failed to send start command")
            return False

        # log("Waiting for camera to begin recording...")

        # Wait for encoder state to turn ON
        import time
        deadline = time.time() + timeout

        while time.time() < deadline:
            if is_recording():
                log("GoPro recording confirmed.")
                return True
            time.sleep(poll_interval)

        print("Timeout: GoPro did not start recording.")
        return False

    except Exception as e:
        print(f"Error starting GoPro recording: {e}")
        return False

def stop_recording():
    """Send command to GoPro to stop recording."""
    try:
        url = f"http://{GOPRO_IP}/gp/gpControl/command/shutter?p=0"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print("GoPro recording stopped")
        else:
            print("Failed to stop recording")
    except Exception as e:
        print(f"Error stopping GoPro recording: {e}")

def get_status():
    """Query GoPro camera status."""
    try:
        url = f"http://{GOPRO_IP}/gp/gpControl/status"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to get GoPro status")
            return None
    except Exception as e:
        print(f"Error getting GoPro status: {e}")
        return None
    
def is_recording():
    """
    Returns True if the GoPro Hero11 Mini is actively recording.
    Uses encoding state ('10') as primary key for accuracy.
    """

    status = get_status()
    if not status:
        return False
    
    print(status.get("status", {}).get("10"))
    
    if status.get("status", {}).get("10") == 1:
        return True

    return False
