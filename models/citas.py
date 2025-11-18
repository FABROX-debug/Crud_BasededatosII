# models/citas.py - VERSIÓN CORREGIDA
from db_oracle import fetch_all, execute_query


def listar_citas():
    query = """
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
        ORDER BY H.FECHA, H.HORA_INICIO
    """
    return fetch_all(query)


def crear_cita(data):
    """Crea una cita y marca el horario como NO disponible"""
    query = """
        INSERT INTO CITAS (
            ID_CITA, ID_PACIENTE, ID_MEDICO, ID_HORARIO, MOTIVO, FECHA_REG
        )
        VALUES (
            SEQ_CITAS.NEXTVAL,
            :id_paciente,
            :id_medico,
            :id_horario,
            :motivo,
            SYSDATE
        )
    """
    execute_query(query, data, commit=True)

    # Marcar horario como NO disponible
    execute_query(
        "UPDATE HORARIOS SET DISPONIBLE = 'N' WHERE ID_HORARIO = :id",
        {"id": data["id_horario"]},
        commit=True
    )


def actualizar_cita(id_cita, data):
    """Actualiza una cita y ajusta disponibilidad de horarios"""
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
    """Elimina una cita y libera el horario"""
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


def horarios_disponibles(id_medico, fecha):
    """Lista horarios disponibles que NO tienen citas asignadas"""
    query = """
        SELECT 
            ID_HORARIO,
            HORA_INICIO,
            HORA_FIN
        FROM HORARIOS
        WHERE ID_MEDICO = :id_medico
          AND FECHA = TO_DATE(:fecha, 'YYYY-MM-DD')
          AND DISPONIBLE = 'S'
        ORDER BY HORA_INICIO
    """
    return fetch_all(query, {
        "id_medico": id_medico,
        "fecha": fecha
    })
