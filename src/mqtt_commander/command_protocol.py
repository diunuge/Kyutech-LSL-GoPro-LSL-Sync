"""
Defines the command protocol and JSON schema for PC → RPi communication.
"""

COMMANDS = {
    "gpio_write": {"pin": int, "value": int},
    "camera_trigger": {"action": str},
    "led_on": {},
    "led_off": {},
    "custom_action": {"params": dict},
}

def validate_command(cmd_type: str, payload: dict) -> bool:
    """
    Validate a command against the protocol.

    Args:
        cmd_type (str): Command name (must exist in COMMANDS)
        payload (dict): Command arguments

    Returns:
        bool: True if valid, False otherwise
    """
    if cmd_type not in COMMANDS:
        return False
    expected_fields = COMMANDS[cmd_type]
    return all(field in payload for field in expected_fields)