"""
Basic MQTT publisher for sending commands to Raspberry Pi devices
"""

import paho.mqtt.client as mqtt
from .config import MQTT_BROKER, MQTT_PORT

def publish(topic: str, message: str):
    """
    Publish a message to a specific MQTT topic.

    Args:
        topic (str): MQTT topic to publish to.
        message (str): Message payload (usually JSON string).
    """
    client = mqtt.Client()
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.publish(topic, message)
    except Exception as e:
        print(f"Error publishing MQTT message: {e}")
    finally:
        client.disconnect()