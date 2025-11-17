# utils/styles.py
# ---------------------------------------------
# Estilos globales de Tkinter/ttk
# ---------------------------------------------

from tkinter import ttk

# Paleta de colores reutilizable
PRIMARY_COLOR = "#1E88E5"
SECONDARY_COLOR = "#0D47A1"
ACCENT_COLOR = "#26C6DA"
BACKGROUND_COLOR = "#F4F6FB"
TEXT_COLOR = "#1F2937"


def apply_styles(root):
    """
    Aplica un estilo moderno y consistente a los controles ttk.
    Se llama una vez desde cada ventana para unificar la interfaz.
    """
    root.configure(bg=BACKGROUND_COLOR)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "TLabel",
        font=("Segoe UI", 10),
        background=BACKGROUND_COLOR,
        foreground=TEXT_COLOR,
    )
    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=6,
        background=PRIMARY_COLOR,
        foreground="white",
        borderwidth=0,
    )
    style.map(
        "TButton",
        background=[("active", SECONDARY_COLOR)],
        foreground=[("disabled", "#D1D5DB")],
    )
    style.configure(
        "Card.TFrame",
        background="white",
        relief="flat",
        borderwidth=1,
    )
    style.configure(
        "Section.TFrame",
        background=BACKGROUND_COLOR,
    )
    style.configure(
        "TCombobox",
        font=("Segoe UI", 10),
        padding=4,
    )
    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=24,
        background="white",
        fieldbackground="white",
        foreground=TEXT_COLOR,
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold"),
        background=PRIMARY_COLOR,
        foreground="white",
    )
