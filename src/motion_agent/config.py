"""
Configuration file for Motion recorder agent
"""

MQTT_BROKER = "localhost"  # Replace with broker IP (commander)
# MQTT_BROKER = "192.168.10.218"  # Replace with broker IP (commander)
MQTT_PORT = 1883
DEVICE_ID = "motion1"        # Unique ID for this motion agent
TOPIC_PREFIX = "rpi"
HEARTBEAT_INTERVAL = 10