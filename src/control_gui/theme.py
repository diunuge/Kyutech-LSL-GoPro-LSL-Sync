"""
Flat, light UI theme + a dark, color-coded console style.
Single place to tweak fonts/colors for the whole app.
"""
from tkinter import ttk

BG = "#F1EFE8"
SURFACE = "#FFFFFF"
BORDER = "#D3D1C7"
TEXT = "#2C2C2A"
TEXT_SECONDARY = "#5F5E5A"

ACCENT = "#185FA5"
ACCENT_ACTIVE = "#0C447C"
ACCENT_LIGHT = "#E6F1FB"

SUCCESS_BG = "#EAF3DE"
SUCCESS_FG = "#27500A"
DANGER_BG = "#FCEBEB"
DANGER_FG = "#791F1F"
WARNING_BG = "#FAEEDA"
WARNING_FG = "#633806"

CONSOLE_BG = "#1E1E1E"
CONSOLE_FG = "#D4D4D4"
CONSOLE_ERROR = "#F2777A"
CONSOLE_WARNING = "#FFCC66"
CONSOLE_SUCCESS = "#99CC99"
CONSOLE_COMMAND = "#6FB1E8"
CONSOLE_MUTED = "#8A8A8A"

FONT_UI = ("Segoe UI", 10)
FONT_UI_BOLD = ("Segoe UI", 10, "bold")
FONT_MONO = ("Consolas", 10)


def apply(root):
    root.configure(bg=BG)

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".", background=BG, foreground=TEXT, font=FONT_UI)
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=TEXT, font=FONT_UI)

    style.configure(
        "TButton", background=SURFACE, foreground=TEXT, font=FONT_UI,
        padding=(10, 6), borderwidth=1, relief="flat", bordercolor=BORDER,
    )
    style.map("TButton", background=[("active", ACCENT_LIGHT)])

    style.configure("Accent.TButton", background=ACCENT, foreground="white")
    style.map("Accent.TButton", background=[("active", ACCENT_ACTIVE)], foreground=[("active", "white")])

    style.configure("Success.TButton", background=SUCCESS_BG, foreground=SUCCESS_FG)
    style.map("Success.TButton", background=[("active", "#DCEFC5")])

    style.configure("Danger.TButton", background=DANGER_BG, foreground=DANGER_FG)
    style.map("Danger.TButton", background=[("active", "#F8D3D3")])

    style.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(0, 4, 0, 0))
    style.configure(
        "TNotebook.Tab", background=BG, foreground=TEXT_SECONDARY,
        padding=(14, 8), font=FONT_UI, borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", SURFACE)],
        foreground=[("selected", TEXT)],
    )

    style.configure(
        "TCombobox", fieldbackground=SURFACE, background=SURFACE,
        foreground=TEXT, arrowcolor=TEXT_SECONDARY, padding=4,
    )

    style.configure(
        "Treeview", background=SURFACE, fieldbackground=SURFACE,
        foreground=TEXT, font=FONT_UI, rowheight=24, borderwidth=0,
    )
    style.configure(
        "Treeview.Heading", background=BG, foreground=TEXT_SECONDARY,
        font=FONT_UI, relief="flat",
    )
    style.map("Treeview", background=[("selected", ACCENT_LIGHT)], foreground=[("selected", TEXT)])

    style.configure("Running.Status.TLabel", background=SUCCESS_BG, foreground=SUCCESS_FG, padding=(8, 3), font=FONT_UI)
    style.configure("Stopped.Status.TLabel", background=BORDER, foreground=TEXT_SECONDARY, padding=(8, 3), font=FONT_UI)
    style.configure("Failed.Status.TLabel", background=DANGER_BG, foreground=DANGER_FG, padding=(8, 3), font=FONT_UI)

    style.configure("Valid.Status.TLabel", background=SUCCESS_BG, foreground=SUCCESS_FG, padding=(8, 3), font=FONT_UI)
    style.configure("Invalid.Status.TLabel", background=DANGER_BG, foreground=DANGER_FG, padding=(8, 3), font=FONT_UI)

    return style


def style_console_widget(text_widget):
    """Applies the dark console look + readability color tags to a tk.Text."""
    text_widget.configure(
        background=CONSOLE_BG,
        foreground=CONSOLE_FG,
        insertbackground=CONSOLE_FG,
        selectbackground=ACCENT,
        selectforeground="white",
        font=FONT_MONO,
        relief="flat",
        padx=8,
        pady=6,
        wrap="word",
    )
    text_widget.tag_configure("error", foreground=CONSOLE_ERROR)
    text_widget.tag_configure("warning", foreground=CONSOLE_WARNING)
    text_widget.tag_configure("success", foreground=CONSOLE_SUCCESS)
    text_widget.tag_configure("command", foreground=CONSOLE_COMMAND)
    text_widget.tag_configure("muted", foreground=CONSOLE_MUTED)


def classify_line(line: str) -> str | None:
    """Picks a readability tag for a line of subprocess output."""
    if line.startswith("$ "):
        return "command"
    lower = line.lower()
    if any(k in lower for k in ("error", "exception", "traceback", "failed", "fail")):
        return "error"
    if "warn" in lower:
        return "warning"
    if any(k in lower for k in ("connected", "success", "started", "running", "exit 0", " ok", "heartbeat")):
        return "success"
    return None
