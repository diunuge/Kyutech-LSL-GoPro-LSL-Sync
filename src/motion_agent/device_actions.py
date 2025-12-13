"""
Define actions that the Raspberry Pi can perform when receiving MQTT commands.
This can include GPIO control, camera triggers, LEDs, motors, etc.
"""

from src.motion_capture.controller import RebocapController

def execute_action(command: dict):
    """
    Execute a command received from MQTT.

    Args:
        command (dict): JSON parsed command payload, e.g.,
            {"cmd": "all_start"}
            {"cmd": "gpio_write", "pin": 17, "value": 1}
    """
    motionController = RebocapController()
    cmd_type = command.get("cmd")

    if cmd_type == "all_start":
        motionController.start()
        print("All Satrting")

    elif cmd_type == "all_stop":
        motionController.stop()
        motionController.close()
        print("All Stoping")
        
    else:
        print(f"[Device Actions] Unknown command: {command}")