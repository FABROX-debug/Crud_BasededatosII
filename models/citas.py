# models/citas.py
from db_oracle import fetch_all, execute_query

# ------------------------------------------------------------
# LISTAR CITAS COMPLETAS
# ------------------------------------------------------------
def listar_citas():
    query = """
        SELECT  C.ID_CITA,
                P.NOMBRE AS PACIENTE,
                M.NOMBRE AS MEDICO,
                M.ESPECIALIDAD,
                TO_CHAR(H.FECHA, 'YYYY-MM-DD') AS FECHA,
                H.ID_HORARIO || ' - ' || TO_CHAR(H.FECHA, 'YYYY-MM-DD') || ' | ' ||
                H.HORA_INICIO || ' a ' || H.HORA_FIN AS HORARIO,
                NVL(C.MOTIVO, '') AS MOTIVO,
                P.ID_PACIENTE,
                M.ID_MEDICO,
                H.ID_HORARIO
        FROM CITAS C
        JOIN PACIENTES P ON P.ID_PACIENTE = C.ID_PACIENTE
        JOIN MEDICOS M   ON M.ID_MEDICO = C.ID_MEDICO
        JOIN HORARIOS H  ON H.ID_HORARIO = C.ID_HORARIO
        ORDER BY H.FECHA, H.HORA_INICIO
    """
    return fetch_all(query)


# ------------------------------------------------------------
# CREAR CITA
# ------------------------------------------------------------
def crear_cita(data):
    query = """
        INSERT INTO CITAS (
            ID_CITA, ID_PACIENTE, ID_MEDICO, ID_HORARIO, MOTIVO, FECHA_REG
        ) VALUES (
            SEQ_CITAS.NEXTVAL,
            :id_paciente,
            :id_medico,
            :id_horario,
            :motivo,
            SYSDATE
        )
    """
    execute_query(query, data, commit=True)


# ------------------------------------------------------------
# ACTUALIZAR CITA
# ------------------------------------------------------------
def actualizar_cita(id_cita, data):
    data["id_cita"] = id_cita
    query = """
        UPDATE CITAS
        SET ID_PACIENTE = :id_paciente,
            ID_MEDICO = :id_medico,
            ID_HORARIO = :id_horario,
            MOTIVO = :motivo
        WHERE ID_CITA = :id_cita
    """
    execute_query(query, data, commit=True)


# ------------------------------------------------------------
# ELIMINAR
# ------------------------------------------------------------
def eliminar_cita(id_cita):
    execute_query(
        "DELETE FROM CITAS WHERE ID_CITA = :id",
        {"id": id_cita},
        commit=True
    )


# ------------------------------------------------------------
# CONSULTA PARA HORARIOS DISPONIBLES SEGÚN MEDICO + FECHA
# ------------------------------------------------------------
def horarios_disponibles(id_medico, fecha):
    return fetch_all("""
        SELECT ID_HORARIO,
               HORA_INICIO || ' - ' || HORA_FIN AS HORARIO
        FROM HORARIOS
        WHERE ID_MEDICO = :id_medico
          AND FECHA = TO_DATE(:fecha, 'YYYY-MM-DD')
          AND DISPONIBLE = 'S'
          AND ID_HORARIO NOT IN (
                SELECT ID_HORARIO FROM CITAS
           )
        ORDER BY HORA_INICIO
    """, {
        "id_medico": id_medico,
        "fecha": fecha
    })
