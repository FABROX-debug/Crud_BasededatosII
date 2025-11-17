# db_config.py
# -----------------------------------------------------------
# CONFIGURACIÓN DE CONEXIÓN A ORACLE DATABASE 21c/18c
# -----------------------------------------------------------
# Reemplaza los valores por tus credenciales reales.
# Este archivo es importado por db_oracle.py

import cx_Oracle

DB_USER = "TU_USUARIO"
DB_PASSWORD = "TU_PASSWORD"

# Por ejemplo: "localhost", "192.168.1.10", "oracle.fisi.edu.pe"
DB_HOST = "TU_HOST"

# Oracle por defecto usa 1521
DB_PORT = 1521

# Nombre del servicio (XE, XEPDB1, ORCL, etc.)
DB_SERVICE = "TU_SERVICIO"


def get_dsn():
    """Genera el DSN para conectar a Oracle."""
    return cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE)
