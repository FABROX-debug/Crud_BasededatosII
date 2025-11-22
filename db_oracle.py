# db_oracle.py
# -----------------------------------------------------------
# Manejo de conexión a Oracle Database 21c/18c
# Funciones para ejecutar SELECT, INSERT, UPDATE y DELETE
# IMPLEMENTACIÓN CON POOL DE CONEXIONES
# -----------------------------------------------------------

import cx_Oracle
from tkinter import messagebox
import atexit

from db_config import DB_USER, DB_PASSWORD, DB_ENCODING, get_dsn

# Variable global para el pool
_pool = None

def init_pool():
    """Inicializa el pool de conexiones si no existe"""
    global _pool
    if _pool is None:
        try:
            dsn = get_dsn()
            _pool = cx_Oracle.SessionPool(
                user=DB_USER,
                password=DB_PASSWORD,
                dsn=dsn,
                min=2,
                max=10,
                increment=1,
                encoding=DB_ENCODING,
                nencoding=DB_ENCODING,
                getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT
            )
            print("Pool de conexiones inicializado correctamente.")
        except cx_Oracle.Error as e:
            print(f"Error al inicializar el pool: {e}")
            # No mostramos messagebox aquí para no bloquear el arranque si es script
            raise e

def close_pool():
    """Cierra el pool de conexiones al salir"""
    global _pool
    if _pool:
        _pool.close()
        _pool = None
        print("Pool de conexiones cerrado.")

# Registrar cierre del pool al salir de la app
atexit.register(close_pool)

# -----------------------------------------------------------
# OBTENER CONEXIÓN
# -----------------------------------------------------------
def get_connection():
    """
    Retorna una conexión activa del pool.
    Si falla, muestra un error visual.
    """
    global _pool
    try:
        if _pool is None:
            init_pool()
        
        # Adquirir conexión del pool
        conn = _pool.acquire()
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

    cur = None
    try:
        cur = conn.cursor()
        cur.execute(query, params or {})
        rows = cur.fetchall()
        return rows

    except cx_Oracle.Error as e:
        messagebox.showerror("Error SQL", f"Error al ejecutar SELECT:\n{e}")
        return []

    finally:
        if cur:
            cur.close()
        if conn:
            # IMPORTANTE: En pool, close() devuelve la conexión al pool
            try:
                _pool.release(conn)
            except:
                pass


# -----------------------------------------------------------
# INSERT / UPDATE / DELETE
# -----------------------------------------------------------
def execute_query(query, params=None, commit=False):
    conn = get_connection()
    if conn is None:
        return

    cur = None
    try:
        cur = conn.cursor()
        cur.execute(query, params or {})

        if commit:
            conn.commit()

    except cx_Oracle.Error as e:
        messagebox.showerror("Error SQL", f"Error en operación:\n{e}")
        # Si hay error, hacemos rollback por seguridad
        try:
            conn.rollback()
        except:
            pass

    finally:
        if cur:
            cur.close()
        if conn:
            try:
                _pool.release(conn)
            except:
                pass
