"""
Main window: python environment bar + a tab per agent/script.
Run with: python -m src.scripts.start_gui
"""
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from src.control_gui import config, theme
from src.control_gui.interpreter_discovery import discover_interpreters, validate_interpreter
from src.control_gui.tabs.gopro_rpi_tab import GoproRpiTab
from src.control_gui.tabs.motion_agent_tab import MotionAgentTab
from src.control_gui.tabs.mqtt_tab import MqttTab
from src.control_gui.tabs.rebocap_tab import RebocapTab

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multimode sensor control panel")
        self.geometry("760x560")
        theme.apply(self)

        self._python_path_var = tk.StringVar()
        self._validity_var = tk.StringVar()
        self._build_env_bar()
        self._build_tabs()

        saved_path = config.load_config().get("python_path")
        initial = saved_path or sys.executable
        self._set_python_path(initial)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_env_bar(self):
        bar = ttk.Frame(self, padding=(10, 8))
        bar.pack(fill="x")

        ttk.Label(bar, text="Environment:").pack(side="left")

        self._interpreters = discover_interpreters(PROJECT_ROOT)
        self._combo = ttk.Combobox(
            bar,
            textvariable=self._python_path_var,
            values=[i.path for i in self._interpreters],
            width=45,
        )
        self._combo.pack(side="left", padx=6, fill="x", expand=True)
        self._combo.bind("<<ComboboxSelected>>", lambda e: self._set_python_path(self._python_path_var.get()))
        self._combo.bind("<Return>", lambda e: self._set_python_path(self._python_path_var.get()))

        ttk.Button(bar, text="Browse...", command=self._browse).pack(side="left", padx=(0, 6))
        self._validity_label = ttk.Label(bar, textvariable=self._validity_var, style="Invalid.Status.TLabel")
        self._validity_label.pack(side="left")

    def _build_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._tabs = [
            MqttTab(notebook, self.get_python_path, PROJECT_ROOT),
            MotionAgentTab(notebook, self.get_python_path, PROJECT_ROOT),
            GoproRpiTab(notebook, self.get_python_path, PROJECT_ROOT),
            RebocapTab(notebook, self.get_python_path, PROJECT_ROOT),
        ]
        titles = ["MQTT control", "Motion agent", "GoPro", "Rebocap test"]
        for tab, title in zip(self._tabs, titles):
            notebook.add(tab, text=title)

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Select python executable",
            filetypes=[("python.exe", "python.exe"), ("all files", "*.*")],
        )
        if path:
            self._set_python_path(path)

    def _set_python_path(self, path: str):
        self._python_path_var.set(path)
        ok, detail = validate_interpreter(path)
        self._validity_var.set(f"valid ({detail})" if ok else f"invalid: {detail}")
        self._validity_label.configure(style="Valid.Status.TLabel" if ok else "Invalid.Status.TLabel")
        if ok:
            config.save_config({"python_path": path})

    def get_python_path(self) -> str:
        return self._python_path_var.get()

    def _on_close(self):
        for tab in self._tabs:
            if tab.is_running():
                tab.terminate()
        self.destroy()


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
