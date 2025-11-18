"""
High-level functions for sending commands to one or many Raspberry Pi devices.
"""

from .mqtt_publisher import publish
from .config import TOPIC_PREFIX

def send_command(device_id: str, cmd: str):
    """
    Send a command to a specific Raspberry Pi device.

    Args:
        device_id (str): Device identifier (matches RPi agent config).
        cmd (str): Command payload (JSON string).
    """
    topic = f"{TOPIC_PREFIX}/{device_id}/cmd"
    publish(topic, cmd)

def broadcast_command(cmd: str):
    """
    Send a command to all devices (broadcast).

    Args:
        cmd (str): Command payload (JSON string).
    """
    topic = f"{TOPIC_PREFIX}/all/cmd"
    publish(topic, cmd)