# utils/styles.py
# ---------------------------------------------
# Estilos globales de Tkinter/ttk - DISEÑO MODERNO
# ---------------------------------------------

from tkinter import ttk

# Paleta de colores moderna (Teal & Slate Theme)
PRIMARY_COLOR = "#0F766E"      # Teal 700
SECONDARY_COLOR = "#0D9488"    # Teal 600
ACCENT_COLOR = "#F59E0B"       # Amber 500
BACKGROUND_COLOR = "#F3F4F6"   # Cool Gray 100
SURFACE_COLOR = "#FFFFFF"      # White
TEXT_COLOR = "#111827"         # Gray 900
TEXT_SECONDARY = "#4B5563"     # Gray 600
ERROR_COLOR = "#EF4444"        # Red 500
SUCCESS_COLOR = "#10B981"      # Emerald 500

def apply_styles(root):
    """
    Aplica un estilo moderno y consistente a los controles ttk.
    """
    root.configure(bg=BACKGROUND_COLOR)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # --- CONFIGURACIÓN GENERAL ---
    style.configure(
        "TLabel",
        font=("Segoe UI", 10),
        background=BACKGROUND_COLOR,
        foreground=TEXT_COLOR,
    )
    
    style.configure(
        "Title.TLabel",
        font=("Segoe UI", 18, "bold"),
        background=BACKGROUND_COLOR,
        foreground=PRIMARY_COLOR,
    )

    style.configure(
        "Subtitle.TLabel",
        font=("Segoe UI", 12),
        background=BACKGROUND_COLOR,
        foreground=TEXT_SECONDARY,
    )

    # --- BOTONES ---
    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        background=PRIMARY_COLOR,
        foreground="white",
        borderwidth=0,
        focuscolor="none"
    )
    style.map(
        "TButton",
        background=[("active", SECONDARY_COLOR), ("disabled", "#9CA3AF")],
        foreground=[("disabled", "#F3F4F6")],
    )
    
    style.configure(
        "Accent.TButton",
        background=ACCENT_COLOR,
        foreground="white"
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#D97706")] # Amber 600
    )

    style.configure(
        "Danger.TButton",
        background=ERROR_COLOR,
        foreground="white"
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#DC2626")] # Red 600
    )

    # --- CONTENEDORES (FRAMES) ---
    style.configure(
        "Card.TFrame",
        background=SURFACE_COLOR,
        relief="flat",
        borderwidth=0,
    )
    
    style.configure(
        "Section.TFrame",
        background=BACKGROUND_COLOR,
    )

    # --- ENTRADAS DE TEXTO ---
    style.configure(
        "TEntry",
        fieldbackground=SURFACE_COLOR,
        foreground=TEXT_COLOR,
        padding=5,
        borderwidth=1,
        relief="solid"
    )
    
    style.configure(
        "TCombobox",
        font=("Segoe UI", 10),
        padding=5,
        fieldbackground=SURFACE_COLOR,
        background=SURFACE_COLOR,
        arrowcolor=TEXT_COLOR
    )

    # --- TABLAS (TREEVIEW) ---
    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=28,
        background=SURFACE_COLOR,
        fieldbackground=SURFACE_COLOR,
        foreground=TEXT_COLOR,
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold"),
        background=PRIMARY_COLOR,
        foreground="white",
        padding=8,
        relief="flat"
    )
    style.map(
        "Treeview",
        background=[("selected", SECONDARY_COLOR)],
        foreground=[("selected", "white")]
    )
    
    # --- SCROLLBARS ---
    style.configure(
        "Vertical.TScrollbar",
        background=BACKGROUND_COLOR,
        troughcolor=BACKGROUND_COLOR,
        borderwidth=0,
        arrowsize=12
    )
