"""
Reusable tab: Start/Terminate buttons, a running/stopped status badge, and a
scrolling console that streams a subprocess's output. Used for any long-running
agent (motion agent, gopro/rpi agent, rebocap sdk test).
"""
import queue
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Callable

from src.control_gui.console_widget import ConsoleText
from src.control_gui.process_runner import ProcessRunner


class BaseProcessTab(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        get_python_path: Callable[[], str],
        cwd: Path,
        argv_builder: Callable[[str], list[str]],
        note: str = "",
    ):
        super().__init__(parent, padding=12)
        self._get_python_path = get_python_path
        self._cwd = cwd
        self._argv_builder = argv_builder
        self._runner = ProcessRunner()

        header = ttk.Frame(self)
        header.pack(fill="x")

        self._status_var = tk.StringVar(value="Stopped")
        self.status_label = ttk.Label(header, textvariable=self._status_var, style="Stopped.Status.TLabel")
        self.status_label.pack(side="left")

        self.start_button = ttk.Button(header, text="Start", style="Success.TButton", command=self._on_start)
        self.start_button.pack(side="right", padx=(6, 0))
        self.terminate_button = ttk.Button(
            header, text="Terminate", style="Danger.TButton", command=self._on_terminate, state="disabled"
        )
        self.terminate_button.pack(side="right")

        console_frame = ttk.Frame(self)
        console_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.console = ConsoleText(console_frame, height=16)
        scrollbar = ttk.Scrollbar(console_frame, command=self.console.yview)
        self.console.configure(yscrollcommand=scrollbar.set)
        self.console.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if note:
            ttk.Label(self, text=note, foreground="#5F5E5A").pack(anchor="w", pady=(6, 0))

        self._poll_queue()

    def _on_start(self):
        if self._runner.is_running():
            return
        python_path = self._get_python_path()
        argv = self._argv_builder(python_path)
        self.console.append(f"$ {' '.join(argv)}")
        try:
            self._runner.start(argv, self._cwd)
        except (RuntimeError, OSError) as exc:
            self.console.append(f"[failed to start] {exc}")
            self._set_status(f"Failed to start", "Failed")
            return
        self.start_button.configure(state="disabled")
        self.terminate_button.configure(state="normal")
        self._set_status(f"Running (pid {self._runner.pid})", "Running")

    def _on_terminate(self):
        self._runner.terminate()
        self.terminate_button.configure(state="disabled")

    def _set_status(self, text: str, kind: str):
        self._status_var.set(text)
        self.status_label.configure(style=f"{kind}.Status.TLabel")

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self._runner.events.get_nowait()
                if kind == "line":
                    self.console.append(payload)
                elif kind == "exit":
                    self.console.append(f"[process exited with code {payload}]")
                    self._set_status(
                        f"Stopped (exit {payload})", "Stopped" if payload == 0 else "Failed"
                    )
                    self.start_button.configure(state="normal")
                    self.terminate_button.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def is_running(self) -> bool:
        return self._runner.is_running()

    def terminate(self):
        self._runner.terminate()
