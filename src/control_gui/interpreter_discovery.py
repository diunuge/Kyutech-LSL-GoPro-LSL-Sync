"""
Finds candidate python interpreters (project venvs + system python) and
validates a chosen interpreter by running `--version` on it directly
(no shell involved).
"""
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

VENV_DIR_NAMES = ("venv", ".venv", "env")


@dataclass
class Interpreter:
    label: str
    path: str


def _venv_python(venv_dir: Path) -> Path:
    return venv_dir / "Scripts" / "python.exe"


def discover_interpreters(project_root: Path) -> list[Interpreter]:
    found: list[Interpreter] = []
    seen: set[str] = set()

    def add(label: str, path: Path):
        if path.is_file():
            resolved = str(path.resolve())
            if resolved not in seen:
                seen.add(resolved)
                found.append(Interpreter(label, resolved))

    for name in VENV_DIR_NAMES:
        venv_dir = project_root / name
        if venv_dir.is_dir():
            add(f"{name} (project)", _venv_python(venv_dir))

    system_python = shutil.which("python")
    if system_python:
        add("system", Path(system_python))

    add("current", Path(sys.executable))

    return found


def validate_interpreter(path: str) -> tuple[bool, str]:
    """Runs `<path> --version` directly (argv list, no shell) to confirm it works."""
    try:
        result = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)

    if result.returncode != 0:
        return False, result.stderr.strip() or "non-zero exit"

    version = (result.stdout or result.stderr).strip()
    return True, version
