import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Callable

from src.control_gui import gopro_ip_tools
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
        self._project_root = project_root
        self._build_ip_panel()

    def _build_ip_panel(self):
        panel = ttk.Frame(self)
        panel.pack(fill="x", before=self.status_label.master, pady=(0, 10))

        row = ttk.Frame(panel)
        row.pack(fill="x")
        ttk.Label(row, text="GoPro USB IP:").pack(side="left")

        self._ip_var = tk.StringVar()
        self._ip_combo = ttk.Combobox(row, textvariable=self._ip_var, width=22)
        self._ip_combo.pack(side="left", padx=6)

        ttk.Button(row, text="Rescan", command=self._rescan).pack(side="left", padx=(0, 6))
        ttk.Button(row, text="Apply", style="Accent.TButton", command=self._apply).pack(side="left")

        self._serial_var = tk.StringVar()
        self._serial_label = ttk.Label(panel, textvariable=self._serial_var, style="Stopped.Status.TLabel")
        self._serial_label.pack(anchor="w", pady=(6, 0))

        self._rescan()
        self._refresh_current_serial()

    def _rescan(self):
        self._ip_combo.configure(values=gopro_ip_tools.discover_candidate_ips())

    def _refresh_current_serial(self):
        serial = gopro_ip_tools.read_current_serial(self._project_root)
        if serial:
            url = gopro_ip_tools.ip_from_serial(serial)
            self._serial_var.set(f"Active serial: {serial} -> {url}:8080")
            self._serial_label.configure(style="Stopped.Status.TLabel")
        else:
            self._serial_var.set("Could not read GOPRO_SERIAL from config.py")
            self._serial_label.configure(style="Failed.Status.TLabel")

    def _apply(self):
        ip = self._ip_var.get().strip()
        serial = gopro_ip_tools.serial_from_ip(ip)
        if serial is None:
            self._serial_var.set(f'"{ip}" doesn\'t match GoPro\'s USB IP pattern (172.2X.1YZ.*)')
            self._serial_label.configure(style="Failed.Status.TLabel")
            return
        gopro_ip_tools.write_serial(self._project_root, serial)
        self._refresh_current_serial()
