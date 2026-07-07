from pathlib import Path
from typing import Callable

from src.control_gui.tabs.base_process_tab import BaseProcessTab

REBOCAP_DIR = "lib/rebocap_python_sdk_v2"
REBOCAP_SCRIPT = "rebocap_ws_sdk_example.py"


class RebocapTab(BaseProcessTab):
    def __init__(self, parent, get_python_path: Callable[[], str], project_root: Path):
        rebocap_dir = project_root / REBOCAP_DIR
        super().__init__(
            parent,
            get_python_path,
            cwd=rebocap_dir,
            argv_builder=lambda python: [python, str(rebocap_dir / REBOCAP_SCRIPT)],
            note="Independent test of the rebocap SDK — can run alongside any other tab",
        )
