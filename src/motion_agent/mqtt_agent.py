"""
MQTT subscriber for the Raspberry Pi.
Listens for commands from the PC commander and executes them.
"""

import json
import time
import paho.mqtt.client as mqtt
from src.motion_agent.device_actions import execute_action
from src.motion_agent.config import MQTT_BROKER, MQTT_PORT, DEVICE_ID, TOPIC_PREFIX

# Topics to listen on
TOPIC_ALL = f"{TOPIC_PREFIX}/all/cmd"
TOPIC_DEVICE = f"{TOPIC_PREFIX}/{DEVICE_ID}/cmd"

# MQTT callback when connected
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    # Subscribe to both device-specific and broadcast topics
    client.subscribe([(TOPIC_ALL, 0), (TOPIC_DEVICE, 0)])

# MQTT callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received command on topic {msg.topic}: {msg.payload.decode()}")
    try:
        command = json.loads(msg.payload.decode())
        execute_action(command)
    except json.JSONDecodeError:
        print("Invalid JSON payload")

# Main function to run the MQTT agent
def run_agent():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    client.loop_start()
    print("Motion agent running, listening for commands...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping agent")
    finally:
        client.loop_stop()
        client.disconnect()

# Run agent if this script is executed directly
if __name__ == '__main__':
    run_agent()