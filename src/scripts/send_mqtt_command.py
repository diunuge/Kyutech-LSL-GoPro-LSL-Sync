"""
Testing script for MQTT command.

use this command in the main folder
python -m src.scripts.send_mqtt_command

"""
from src.mqtt_commander.commander import send_command

# python -m src.scripts.send_mqtt_command

if __name__ == '__main__':
    # Send a test command to RPi device rpi1
    send_command("rpi1", '{"cmd":"gpio_write","pin":17,"value":1}')
    print("Command sent to rpi1")