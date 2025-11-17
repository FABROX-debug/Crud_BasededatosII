# utils/styles.py
# ---------------------------------------------
# Estilos globales de Tkinter/ttk
# ---------------------------------------------

from tkinter import ttk

def apply_styles(root):
    """
    Aplica un estilo básico a ttk para que se vea más moderno.
    Se llama una vez desde main.py.
    """
    style = ttk.Style(root)
    try:
        # Si está disponible, usar un tema más moderno
        style.theme_use("clam")
    except:
        # Si falla, deja el default
        pass

    style.configure(
        "TLabel",
        font=("Segoe UI", 10)
    )
    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=5
    )
    style.configure(
        "TCombobox",
        font=("Segoe UI", 10)
    )
    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=22
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold")
    )
