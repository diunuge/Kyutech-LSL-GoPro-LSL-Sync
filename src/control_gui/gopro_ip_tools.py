"""
Converts between a GoPro's USB (RNDIS) IP address and the 3-digit serial
suffix used in src/gopro_lsl/config.py, and discovers candidate IPs from the
machine's own network adapters.

Mirrors the formula in src/gopro_lsl/gopro_control.py:
    x = serial_last3[0]; yz = serial_last3[1:]
    camera_ip = f"172.2{x}.1{yz}.51"
"""
import re
import subprocess
from pathlib import Path

IP_PATTERN = re.compile(r"^172\.2(\d)\.1(\d{2})\.\d{1,3}$")
IPV4_LINE_PATTERN = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")
SERIAL_LINE_PATTERN = re.compile(r'^(GOPRO_SERIAL\s*=\s*)"(\d{3})"(.*)$', re.MULTILINE)

CONFIG_PATH_PARTS = ("src", "gopro_lsl", "config.py")


def serial_from_ip(ip: str) -> str | None:
    """Returns the 3-digit serial suffix if `ip` matches GoPro's USB scheme, else None."""
    match = IP_PATTERN.match(ip.strip())
    if not match:
        return None
    x, yz = match.groups()
    return f"{x}{yz}"


def ip_from_serial(serial_last3: str) -> str:
    x = serial_last3[0]
    yz = serial_last3[1:]
    return f"172.2{x}.1{yz}.51"


def discover_candidate_ips() -> list[str]:
    """Runs `ipconfig` (no shell) and returns IPv4 addresses matching GoPro's USB subnet."""
    try:
        result = subprocess.run(
            ["ipconfig"], capture_output=True, text=True, timeout=5
        )
    except (OSError, subprocess.TimeoutExpired):
        return []

    candidates = []
    for match in IPV4_LINE_PATTERN.finditer(result.stdout):
        ip = match.group(1)
        if serial_from_ip(ip) is not None and ip not in candidates:
            candidates.append(ip)
    return candidates


def _config_path(project_root: Path) -> Path:
    return project_root.joinpath(*CONFIG_PATH_PARTS)


def read_current_serial(project_root: Path) -> str | None:
    text = _config_path(project_root).read_text(encoding="utf-8")
    match = SERIAL_LINE_PATTERN.search(text)
    return match.group(2) if match else None


def write_serial(project_root: Path, new_serial: str) -> None:
    config_path = _config_path(project_root)
    text = config_path.read_text(encoding="utf-8")
    new_text, count = SERIAL_LINE_PATTERN.subn(rf'\g<1>"{new_serial}"\g<3>', text)
    if count == 0:
        raise ValueError("GOPRO_SERIAL assignment not found in config.py")
    config_path.write_text(new_text, encoding="utf-8")
