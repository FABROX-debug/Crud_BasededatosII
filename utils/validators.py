# utils/validators.py
# ---------------------------------------------
# Validaciones básicas
# ---------------------------------------------

from datetime import datetime

def es_fecha_valida(fecha_str, formato="%Y-%m-%d"):
    """
    Valida si una cadena tiene formato de fecha correcto.
    Por defecto: 'YYYY-MM-DD'.
    """
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except ValueError:
        return False
