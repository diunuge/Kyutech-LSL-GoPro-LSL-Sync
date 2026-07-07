"""
MQTT broadcast start/stop tab. Each click is a one-shot run of the
corresponding send_mqtt_broadcast_* script; since agents don't send an ack,
users may need to click Start/Stop more than once, so every attempt (and its
exit code) is kept in a visible history.
"""
import queue
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import ttk
from typing import Callable

from src.control_gui import theme
from src.control_gui.process_runner import ProcessRunner

MAX_HISTORY = 50


class MqttTab(ttk.Frame):
    def __init__(self, parent, get_python_path: Callable[[], str], project_root: Path):
        super().__init__(parent, padding=12)
        self._get_python_path = get_python_path
        self._project_root = project_root
        self._runner: ProcessRunner | None = None
        self._pending_label = ""

        buttons = ttk.Frame(self)
        buttons.pack(fill="x")
        ttk.Button(
            buttons, text="Broadcast start", style="Success.TButton",
            command=lambda: self._send("all_start", "src.scripts.send_mqtt_broadcast_start"),
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(
            buttons, text="Broadcast stop", style="Danger.TButton",
            command=lambda: self._send("all_stop", "src.scripts.send_mqtt_broadcast_stop"),
        ).pack(side="left", fill="x", expand=True)

        status = ttk.Frame(self)
        status.pack(fill="x", pady=(12, 6))
        self._last_command_var = tk.StringVar(value="(none yet)")
        self._last_result_var = tk.StringVar(value="")
        ttk.Label(status, text="Last command:").pack(side="left")
        ttk.Label(status, textvariable=self._last_command_var).pack(side="left", padx=(4, 12))
        self._result_label = ttk.Label(status, textvariable=self._last_result_var, style="Stopped.Status.TLabel")
        self._result_label.pack(side="left")

        ttk.Label(self, text="Send history (retry if an agent didn't pick it up):").pack(
            anchor="w"
        )
        history_frame = ttk.Frame(self)
        history_frame.pack(fill="both", expand=True, pady=(4, 0))
        columns = ("time", "command", "result")
        self.history = ttk.Treeview(
            history_frame, columns=columns, show="headings", height=10
        )
        for col, width in (("time", 90), ("command", 120), ("result", 260)):
            self.history.heading(col, text=col.capitalize())
            self.history.column(col, width=width, anchor="w")
        scrollbar = ttk.Scrollbar(history_frame, command=self.history.yview)
        self.history.configure(yscrollcommand=scrollbar.set)
        self.history.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.history.tag_configure("ok", foreground=theme.SUCCESS_FG)
        self.history.tag_configure("bad", foreground=theme.DANGER_FG)

    def _send(self, label: str, module: str):
        if self._runner is not None and self._runner.is_running():
            return
        python_path = self._get_python_path()
        argv = [python_path, "-m", module]
        self._pending_label = label
        self._runner = ProcessRunner()
        self._last_command_var.set(label)
        self._last_result_var.set("sending...")
        self._result_label.configure(style="Stopped.Status.TLabel")
        try:
            self._runner.start(argv, self._project_root)
        except (RuntimeError, OSError) as exc:
            self._record(label, f"failed to start: {exc}")
            return
        self.after(100, self._poll)

    def _poll(self):
        try:
            while True:
                kind, payload = self._runner.events.get_nowait()
                if kind == "exit":
                    result = "exit 0" if payload == 0 else f"exit {payload}"
                    self._record(self._pending_label, result)
                    return
        except queue.Empty:
            pass
        self.after(100, self._poll)

    def _record(self, label: str, result: str):
        self._last_result_var.set(result)
        self._result_label.configure(
            style="Running.Status.TLabel" if result == "exit 0" else "Failed.Status.TLabel"
        )
        timestamp = datetime.now().strftime("%H:%M:%S")
        row_tag = "ok" if result == "exit 0" else "bad"
        self.history.insert("", 0, values=(timestamp, label, result), tags=(row_tag,))
        children = self.history.get_children()
        if len(children) > MAX_HISTORY:
            self.history.delete(children[-1])

    def is_running(self) -> bool:
        return self._runner is not None and self._runner.is_running()

    def terminate(self):
        if self._runner is not None:
            self._runner.terminate()
