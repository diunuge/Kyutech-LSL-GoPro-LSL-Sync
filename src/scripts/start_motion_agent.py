"""
Launcher script for Motion agent.
Starts the MQTT command listener.
"""

import atexit
from src.motion_agent.mqtt_agent import run_agent
from src.log.logger import logger

def main():

    atexit.register(logger.close)

    try:
        # Run the MQTT agent (blocking)
        run_agent()
    except KeyboardInterrupt:
        print("Stopping agent...")
    finally:
        print("Agent exited.")

if __name__ == '__main__':
    main()