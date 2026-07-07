"""
Read-only, color-coded, copyable console for streaming subprocess output.
"""
import tkinter as tk

from src.control_gui import theme


class ConsoleText(tk.Text):
    def __init__(self, parent, **kwargs):
        kwargs.setdefault("height", 16)
        kwargs.setdefault("state", "disabled")
        super().__init__(parent, **kwargs)
        theme.style_console_widget(self)
        self._build_context_menu()
        self.bind("<Control-c>", self._copy)
        self.bind("<Control-a>", self._select_all)
        self.bind("<Button-3>", self._show_context_menu)

    def append(self, line: str):
        tag = theme.classify_line(line)
        self.configure(state="normal")
        self.insert("end", line + "\n", (tag,) if tag else ())
        self.see("end")
        self.configure(state="disabled")

    def clear(self):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")

    def _build_context_menu(self):
        self._menu = tk.Menu(self, tearoff=0)
        self._menu.add_command(label="Copy", command=self._copy)
        self._menu.add_command(label="Select all", command=self._select_all)
        self._menu.add_separator()
        self._menu.add_command(label="Clear", command=self.clear)

    def _show_context_menu(self, event):
        self._menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def _copy(self, event=None):
        try:
            selected = self.get("sel.first", "sel.last")
        except tk.TclError:
            selected = self.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(selected)
        return "break"

    def _select_all(self, event=None):
        self.tag_add("sel", "1.0", "end")
        return "break"
