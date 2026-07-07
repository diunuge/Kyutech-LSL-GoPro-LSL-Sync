from pathlib import Path
from typing import Callable

from src.control_gui.tabs.base_process_tab import BaseProcessTab


class GoproRpiTab(BaseProcessTab):
    def __init__(self, parent, get_python_path: Callable[[], str], project_root: Path):
        super().__init__(
            parent,
            get_python_path,
            cwd=project_root,
            argv_builder=lambda python: [
                python,
                "-m",
                "src.scripts.start_rpi_agent_with_heartbeat",
            ],
            note="Runs on the RPi-connected machine — start_rpi_agent_with_heartbeat.py",
        )
