"""
Persistence for GUI settings (currently just the selected python interpreter).
"""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / ".gui_config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(data: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
