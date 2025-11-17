# db_oracle.py
# -----------------------------------------------------------
# MANEJO DE CONEXIÓN A ORACLE DATABASE 21c/18c
# Funciones para ejecutar SELECT, INSERT, UPDATE y DELETE
# -----------------------------------------------------------

import cx_Oracle
from db_config import DB_USER, DB_PASSWORD, get_dsn
from tkinter import messagebox

# -----------------------------------------------------------
# OBTENER CONEXIÓN
# -----------------------------------------------------------
def get_connection():
    """
    Retorna una conexión activa a Oracle.
    Si falla la conexión, muestra un error visual.
    """
    try:
        conn = cx_Oracle.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=get_dsn()
        )
        return conn

    except cx_Oracle.Error as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a Oracle:\n{e}")
        return None


# -----------------------------------------------------------
# SELECT (DEVUELVE LISTA DE TUPLAS)
# -----------------------------------------------------------
def fetch_all(query, params=None):
    conn = get_connection()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        cur.execute(query, params or {})
        rows = cur.fetchall()
        return rows

    except cx_Oracle.Error as e:
        messagebox.showerror("Error SQL", f"Error al ejecutar SELECT:\n{e}")
        return []

    finally:
        cur.close()
        conn.close()


# -----------------------------------------------------------
# INSERT / UPDATE / DELETE
# -----------------------------------------------------------
def execute_query(query, params=None, commit=False):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute(query, params or {})

        if commit:
            conn.commit()

    except cx_Oracle.Error as e:
        messagebox.showerror("Error SQL", f"Error en operación:\n{e}")

    finally:
        cur.close()
        conn.close()
