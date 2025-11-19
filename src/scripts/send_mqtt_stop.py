"""
Testing script for MQTT command.

use this command in the main folder

"""
from src.mqtt_commander.commander import send_command

# python -m src.scripts.send_mqtt_command

if __name__ == '__main__':
    # Send a test command to RPi device rpi1
    send_command("rpi1", '{"cmd":"camera_stop"}')
    print("Command sent to rpi1")