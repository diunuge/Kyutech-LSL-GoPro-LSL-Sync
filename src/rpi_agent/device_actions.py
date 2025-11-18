"""
Define actions that the Raspberry Pi can perform when receiving MQTT commands.
This can include GPIO control, camera triggers, LEDs, motors, etc.
"""

def execute_action(command: dict):
    """
    Execute a command received from MQTT.

    Args:
        command (dict): JSON parsed command payload, e.g.,
            {"cmd": "gpio_write", "pin": 17, "value": 1}
    """
    cmd_type = command.get("cmd")

    if cmd_type == "gpio_write":
        pin = command.get("pin")
        value = command.get("value")
        print(f"[Device Actions] GPIO write: pin={pin}, value={value}")
        # TODO: implement actual GPIO control using RPi.GPIO or gpiozero

    elif cmd_type == "led_on":
        print("[Device Actions] LED ON")
        # TODO: implement LED on

    elif cmd_type == "led_off":
        print("[Device Actions] LED OFF")
        # TODO: implement LED off

    elif cmd_type == "camera_start":
        print("[Device Actions] Camera Started")
        # TODO: start camera

    elif cmd_type == "camera_stop":
        print("[Device Actions] Camera Stopped")
        # TODO: stop camera

    else:
        print(f"[Device Actions] Unknown command: {command}")