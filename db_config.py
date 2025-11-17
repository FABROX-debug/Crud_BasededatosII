# db_config.py
"""
Configuración centralizada para la conexión a Oracle Database.
Los valores pueden sobreescribirse mediante variables de entorno,
lo que facilita la configuración en diferentes entornos.
"""

import os

DB_USER = os.getenv("DB_USER", "CITA_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "cita123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 1521))
DB_SERVICE = os.getenv("DB_SERVICE", "XEPDB1")
DB_ENCODING = os.getenv("DB_ENCODING", "UTF-8")


def get_dsn():
    """
    Construye un descriptor de servicio (DSN) válido para Oracle.
    Se utiliza la utilidad nativa de cx_Oracle para evitar errores de formato.
    """
    import cx_Oracle  # import local para evitar dependencias en tiempo de carga

    return cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE)
