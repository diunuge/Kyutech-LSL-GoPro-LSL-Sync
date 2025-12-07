"""
Launcher script for Raspberry Pi agent.
Starts both the MQTT command listener and the heartbeat thread.
"""

import atexit
from src.rpi_agent.mqtt_agent import run_agent
from src.rpi_agent.heartbeat import Heartbeat
from src.log.logger import logger

def main():

    atexit.register(logger.close)

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