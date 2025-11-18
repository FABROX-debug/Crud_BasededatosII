# models/horarios.py
from db_oracle import fetch_all, execute_query

# -----------------------------
# LISTAR HORARIOS DISPONIBLES
# -----------------------------
def listar_horarios_disponibles(id_medico, fecha_str):
    query = """
        SELECT ID_HORARIO,
               TO_CHAR(FECHA, 'YYYY-MM-DD') AS FECHA,
               HORA_INICIO,
               HORA_FIN
        FROM HORARIOS
        WHERE ID_MEDICO = :id_medico
          AND FECHA = TO_DATE(:fecha, 'YYYY-MM-DD')
          AND DISPONIBLE = 'S'
          AND ID_HORARIO NOT IN (
                SELECT ID_HORARIO FROM CITAS
          )
        ORDER BY HORA_INICIO
    """
    return fetch_all(query, {
        "id_medico": id_medico,
        "fecha": fecha_str
    })


# -----------------------------
# LISTAR TODOS LOS HORARIOS (CRUD)
# -----------------------------
def listar_horarios():
    query = """
        SELECT H.ID_HORARIO,
               M.NOMBRE AS MEDICO,
               TO_CHAR(H.FECHA, 'YYYY-MM-DD'),
               H.HORA_INICIO,
               H.HORA_FIN,
               H.DISPONIBLE
        FROM HORARIOS H
        JOIN MEDICOS M ON M.ID_MEDICO = H.ID_MEDICO
        ORDER BY H.FECHA, H.HORA_INICIO
    """
    return fetch_all(query)


# -----------------------------
# CREAR HORARIO
# -----------------------------
def crear_horario(data):
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


# -----------------------------
# ACTUALIZAR HORARIO
# -----------------------------
def actualizar_horario(id_horario, data):
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


# -----------------------------
# ELIMINAR HORARIO
# -----------------------------
def eliminar_horario(id_horario):
    execute_query(
        "DELETE FROM HORARIOS WHERE ID_HORARIO = :id",
        {"id": id_horario},
        commit=True
    )
