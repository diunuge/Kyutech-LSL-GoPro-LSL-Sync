"""
Optional heartbeat: publishes alive messages to MQTT broker at regular intervals.
Useful for monitoring Raspberry Pi health/status.
"""

import time
import json
import threading
import paho.mqtt.client as mqtt
from src.rpi_agent.config import MQTT_BROKER, MQTT_PORT, DEVICE_ID, TOPIC_PREFIX, HEARTBEAT_INTERVAL

HEARTBEAT_TOPIC = f"{TOPIC_PREFIX}/{DEVICE_ID}/heartbeat"

class Heartbeat(threading.Thread):
    """
    Thread that sends periodic heartbeat messages to the MQTT broker.
    """
    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.running = True

    def run(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT)
            self.client.loop_start()
            while self.running:
                payload = json.dumps({
                    "device_id": DEVICE_ID,
                    "status": "alive",
                    "timestamp": time.time()
                })
                self.client.publish(HEARTBEAT_TOPIC, payload)
                time.sleep(HEARTBEAT_INTERVAL)
        except Exception as e:
            print(f"Heartbeat error: {e}")
        finally:
            self.client.loop_stop()
            self.client.disconnect()

    def stop(self):
        """
        Stop the heartbeat thread.
        """
        self.running = False

# Run heartbeat if executed directly
if __name__ == '__main__':
    hb = Heartbeat()
    hb.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        hb.stop()