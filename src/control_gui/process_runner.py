"""
Runs a child process (given as an argv list, never via a shell) and streams
its combined stdout/stderr back through a thread-safe queue so a Tkinter
widget can poll it with `.after(...)`.
"""
import os
import queue
import subprocess
import threading
from pathlib import Path

_CREATIONFLAGS = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


class ProcessRunner:
    """One subprocess at a time. Not reusable across overlapping runs."""

    def __init__(self):
        self.events: "queue.Queue[tuple[str, object]]" = queue.Queue()
        self._process: subprocess.Popen | None = None
        self._reader_thread: threading.Thread | None = None

    def is_running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    @property
    def pid(self) -> int | None:
        return self._process.pid if self._process else None

    def start(self, argv: list[str], cwd: Path) -> None:
        if self.is_running():
            raise RuntimeError("a process is already running")

        env = dict(
            os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONUNBUFFERED="1"
        )
        # argv[0] is always the python interpreter (see tabs/*_tab.py argv_builders).
        # -u forces unbuffered stdout so print() ordering matches a real console
        # instead of being stuck in a block buffer because stdout is a pipe here.
        argv = [argv[0], "-u", *argv[1:]]

        self._process = subprocess.Popen(
            argv,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            creationflags=_CREATIONFLAGS,
        )
        self._reader_thread = threading.Thread(target=self._read_output, daemon=True)
        self._reader_thread.start()

    def _read_output(self) -> None:
        process = self._process
        assert process is not None and process.stdout is not None
        for line in iter(process.stdout.readline, ""):
            self.events.put(("line", line.rstrip("\n")))
        process.stdout.close()
        exit_code = process.wait()
        self.events.put(("exit", exit_code))

    def terminate(self) -> None:
        if not self.is_running():
            return
        self._process.terminate()

        def _force_kill_if_needed():
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()

        threading.Thread(target=_force_kill_if_needed, daemon=True).start()
