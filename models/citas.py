# =====================================================
import cx_Oracle
from db_oracle import fetch_all, execute_query, get_connection
from tkinter import messagebox

def listar_citas():
    # Query completa
    query_full = """
        SELECT  
            C.ID_CITA,
            P.NOMBRE AS PACIENTE,
            M.NOMBRE AS MEDICO,
            M.ESPECIALIDAD,
            TO_CHAR(H.FECHA, 'YYYY-MM-DD') AS FECHA,
            H.HORA_INICIO || ' - ' || H.HORA_FIN AS HORARIO,
            NVL(C.MOTIVO, '-') AS MOTIVO,
            TO_CHAR(C.FECHA_REG, 'YYYY-MM-DD HH24:MI') AS FECHA_REG
        FROM CITAS C
        JOIN PACIENTES P ON P.ID_PACIENTE = C.ID_PACIENTE
        JOIN MEDICOS M   ON M.ID_MEDICO = C.ID_MEDICO
        JOIN HORARIOS H  ON H.ID_HORARIO = C.ID_HORARIO
        ORDER BY H.FECHA DESC, H.HORA_INICIO
    """

    # Query de respaldo (sin FECHA_REG)
    query_fallback = """
        SELECT  
            C.ID_CITA,
            P.NOMBRE AS PACIENTE,
            M.NOMBRE AS MEDICO,
            M.ESPECIALIDAD,
            TO_CHAR(H.FECHA, 'YYYY-MM-DD') AS FECHA,
            H.HORA_INICIO || ' - ' || H.HORA_FIN AS HORARIO,
            NVL(C.MOTIVO, '-') AS MOTIVO,
            '-' AS FECHA_REG
        FROM CITAS C
        JOIN PACIENTES P ON P.ID_PACIENTE = C.ID_PACIENTE
        JOIN MEDICOS M   ON M.ID_MEDICO = C.ID_MEDICO
        JOIN HORARIOS H  ON H.ID_HORARIO = C.ID_HORARIO
        ORDER BY H.FECHA DESC, H.HORA_INICIO
    """

    conn = get_connection()
    if conn is None:
        return []

    cur = None
    try:
        cur = conn.cursor()
        cur.execute(query_full)
        rows = cur.fetchall()
        return rows

    except cx_Oracle.DatabaseError as e:
        error_obj, = e.args
        # Si el error es "invalid identifier" (ORA-00904), probamos el fallback
        if error_obj.code == 904: 
            try:
                print("Advertencia: Columna FECHA_REG no encontrada. Usando query de respaldo.")
                cur.execute(query_fallback)
                rows = cur.fetchall()
                return rows
            except cx_Oracle.Error as e2:
                messagebox.showerror("Error SQL", f"Error al ejecutar SELECT (Fallback):\n{e2}")
                return []
        else:
            messagebox.showerror("Error SQL", f"Error al ejecutar SELECT:\n{e}")
            return []

    finally:
        if cur:
            cur.close()
        if conn:
            try:
                # Asumiendo que get_connection usa el pool del db_oracle modificado
                # Si no, esto podría fallar si no se importó _pool, pero db_oracle maneja el release en close() si es objeto conexión?
                # En el código anterior de db_oracle.py, get_connection devuelve el objeto conexión raw del pool.
                # Debemos hacer release.
                # Como no tenemos acceso a _pool aquí directamente, dependemos de cómo db_oracle maneja el cierre.
                # Revisando db_oracle.py: fetch_all hace _pool.release(conn).
                # Aquí estamos haciendo manual.
                # Necesitamos acceder al pool o llamar a close().
                # Si es cx_Oracle.Connection del pool, .close() lo devuelve al pool?
                # Sí, en SessionPool, conn.close() libera la conexión al pool.
                conn.close()
            except:
                pass


def crear_cita(data):
    query = """
        INSERT INTO CITAS (
            ID_PACIENTE, ID_MEDICO, ID_HORARIO, MOTIVO
        )
        VALUES (
            :id_paciente,
            :id_medico,
            :id_horario,
            :motivo
        )
    """
    execute_query(query, data, commit=True)

    # NOTA: El trigger TRG_ACTUALIZAR_HORARIO_CITA se encarga de poner DISPONIBLE='N'


def actualizar_cita(id_cita, data):
    # Obtener horario anterior
    horario_anterior = fetch_all(
        "SELECT ID_HORARIO FROM CITAS WHERE ID_CITA = :id",
        {"id": id_cita}
    )

    data["id_cita"] = id_cita
    query = """
        UPDATE CITAS
        SET 
            ID_PACIENTE = :id_paciente,
            ID_MEDICO   = :id_medico,
            ID_HORARIO  = :id_horario,
            MOTIVO      = :motivo
        WHERE ID_CITA   = :id_cita
    """
    execute_query(query, data, commit=True)

    # Liberar horario anterior si cambió
    if horario_anterior and horario_anterior[0][0] != data["id_horario"]:
        execute_query(
            "UPDATE HORARIOS SET DISPONIBLE = 'S' WHERE ID_HORARIO = :id",
            {"id": horario_anterior[0][0]},
            commit=True
        )

        # Marcar nuevo horario como ocupado
        execute_query(
            "UPDATE HORARIOS SET DISPONIBLE = 'N' WHERE ID_HORARIO = :id",
            {"id": data["id_horario"]},
            commit=True
        )


def eliminar_cita(id_cita):
    # Obtener horario antes de eliminar
    horario = fetch_all(
        "SELECT ID_HORARIO FROM CITAS WHERE ID_CITA = :id",
        {"id": id_cita}
    )

    execute_query(
        "DELETE FROM CITAS WHERE ID_CITA = :id",
        {"id": id_cita},
        commit=True
    )

    # Liberar horario
    if horario:
        execute_query(
            "UPDATE HORARIOS SET DISPONIBLE = 'S' WHERE ID_HORARIO = :id",
            {"id": horario[0][0]},
            commit=True
        )
