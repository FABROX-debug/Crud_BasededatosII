import cx_Oracle
from db_config import DB_USER, DB_PASSWORD, get_dsn

try:
    conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, get_dsn())
    print("Conexión exitosa! ✔")
    conn.close()
except Exception as e:
    print("Error:", e)
