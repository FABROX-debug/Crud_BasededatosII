import cx_Oracle
from db_config import DB_USER, DB_PASSWORD, get_dsn

conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, get_dsn())
cur = conn.cursor()

cur.execute("SELECT USER FROM dual")
print("Conectado como:", cur.fetchone()[0])

conn.close()
