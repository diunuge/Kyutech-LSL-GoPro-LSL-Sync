"""
Configuration file for Raspberry Pi agent
"""

MQTT_BROKER = "192.168.10.218"  # Replace with broker IP (commander)
MQTT_PORT = 1883
DEVICE_ID = "rpi1"        # Unique ID for this Raspberry Pi
TOPIC_PREFIX = "rpi"
HEARTBEAT_INTERVAL = 10