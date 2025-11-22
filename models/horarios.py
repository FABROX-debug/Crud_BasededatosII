# models/horarios.py - VERSIÓN CORREGIDA V2
from db_oracle import fetch_all, execute_query


def listar_fechas_por_medico(id_medico):
    """Lista fechas disponibles para un médico específico"""
    return fetch_all("""
        SELECT DISTINCT TO_CHAR(FECHA, 'YYYY-MM-DD') AS FECHA
        FROM HORARIOS
        WHERE ID_MEDICO = :id_medico
        ORDER BY 1
    """, {"id_medico": id_medico})


def listar_horarios_por_medico_y_fecha(id_medico, fecha):
    """Lista horarios disponibles para un médico en una fecha específica"""
    return fetch_all("""
        SELECT ID_HORARIO,
               HORA_INICIO,
               HORA_FIN
        FROM HORARIOS
        WHERE ID_MEDICO = :id_medico
          AND FECHA = TO_DATE(:fecha, 'YYYY-MM-DD')
          AND DISPONIBLE = 'S'
        ORDER BY HORA_INICIO
    """, {
        "id_medico": id_medico,
        "fecha": fecha
    })


def listar_horarios():
    """Lista TODOS los horarios con información del médico - FORMATO MEJORADO"""
    return fetch_all("""
        SELECT H.ID_HORARIO,
               H.ID_MEDICO,
               M.NOMBRE AS MEDICO_NOMBRE,
               M.ESPECIALIDAD,
               TO_CHAR(H.FECHA, 'YYYY-MM-DD') AS FECHA,
               H.HORA_INICIO,
               H.HORA_FIN,
               H.DISPONIBLE
        FROM HORARIOS H
        JOIN MEDICOS M ON M.ID_MEDICO = H.ID_MEDICO
        ORDER BY H.FECHA, H.HORA_INICIO
    """)


def listar_horarios_por_medico(id_medico):
    """Lista horarios de un médico específico - NUEVA FUNCIÓN"""
    return fetch_all("""
        SELECT H.ID_HORARIO,
               TO_CHAR(H.FECHA, 'YYYY-MM-DD') AS FECHA,
               H.HORA_INICIO,
               H.HORA_FIN,
               H.DISPONIBLE
        FROM HORARIOS H
        WHERE H.ID_MEDICO = :id_medico
        ORDER BY H.FECHA, H.HORA_INICIO
    """, {"id_medico": id_medico})


def crear_horario(data):
    """Crea un nuevo horario"""
    query = """
        INSERT INTO HORARIOS (
            ID_HORARIO,
            ID_MEDICO,
            FECHA,
            HORA_INICIO,
            HORA_FIN,
            DISPONIBLE
        )
        VALUES (
            SEQ_HORARIOS.NEXTVAL,
            :id_medico,
            TO_DATE(:fecha, 'YYYY-MM-DD'),
            :hora_inicio,
            :hora_fin,
            :disponible
        )
    """
    execute_query(query, data, commit=True)


def actualizar_horario(id_horario, data):
    """Actualiza un horario existente"""
    data["id"] = id_horario
    query = """
        UPDATE HORARIOS
        SET ID_MEDICO = :id_medico,
            FECHA = TO_DATE(:fecha, 'YYYY-MM-DD'),
            HORA_INICIO = :hora_inicio,
            HORA_FIN = :hora_fin,
            DISPONIBLE = :disponible
        WHERE ID_HORARIO = :id
    """
    execute_query(query, data, commit=True)


def eliminar_horario(id_horario):
    """Elimina un horario"""
    execute_query(
        "DELETE FROM HORARIOS WHERE ID_HORARIO = :id",
        {"id": id_horario},
        commit=True
    )