# db_config.py
print("USANDO db_config.py:", __file__)

DB_USER = "CITA_USER"
DB_PASSWORD = "cita123"
DB_HOST = "localhost"
DB_PORT = 1521
DB_SERVICE = "XEPDB1"


def get_dsn():
    return f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={DB_HOST})(PORT={DB_PORT}))(CONNECT_DATA=(SERVICE_NAME={DB_SERVICE})))"
