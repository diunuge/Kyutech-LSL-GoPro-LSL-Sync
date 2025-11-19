"""
GoPro control module.
Provides functions to start and stop recording and query camera status.
"""

import requests

# Example default GoPro IP
GOPRO_IP = "10.5.5.9"

def start_recording():
    """Send command to GoPro to start recording."""
    try:
        url = f"http://{GOPRO_IP}/gp/gpControl/command/shutter?p=1"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print("GoPro recording started")
        else:
            print("Failed to start recording")
    except Exception as e:
        print(f"Error starting GoPro recording: {e}")

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