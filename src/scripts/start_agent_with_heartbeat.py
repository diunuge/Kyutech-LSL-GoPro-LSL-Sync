# src/rpi_agent/start_agent_with_heartbeat.py
"""
Launcher script for Raspberry Pi agent.
Starts both the MQTT command listener and the heartbeat thread.
"""

import threading
import time
from src.rpi_agent.mqtt_agent import run_agent
from src.rpi_agent.heartbeat import Heartbeat

def main():
    # Start the heartbeat thread
    hb = Heartbeat()
    hb.start()
    print("Heartbeat thread started")

    try:
        # Run the MQTT agent (blocking)
        run_agent()
    except KeyboardInterrupt:
        print("Stopping agent and heartbeat...")
    finally:
        # Stop the heartbeat thread gracefully
        hb.stop()
        hb.join()
        print("Heartbeat stopped. Agent exited.")

if __name__ == '__main__':
    main()