# models/horarios.py
from db_oracle import fetch_all, execute_query

# -----------------------------
# LISTAR HORARIOS DISPONIBLES
# -----------------------------
def listar_horarios_disponibles(id_medico, fecha_str):
    query = """
        SELECT ID_HORARIO,
               TO_CHAR(HORA_INICIO, 'HH24:MI'),
               TO_CHAR(HORA_FIN, 'HH24:MI')
        FROM HORARIOS
        WHERE ID_MEDICO = :id_medico
          AND FECHA = TO_DATE(:fecha, 'YYYY-MM-DD')
          AND DISPONIBLE = 'S'
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
               U.NOMBRE AS MEDICO,
               TO_CHAR(H.FECHA, 'YYYY-MM-DD'),
               TO_CHAR(H.HORA_INICIO, 'HH24:MI'),
               TO_CHAR(H.HORA_FIN, 'HH24:MI'),
               H.DISPONIBLE
        FROM HORARIOS H
        JOIN MEDICOS M ON M.ID_MEDICO = H.ID_MEDICO
        JOIN USUARIOS U ON U.ID_USUARIO = M.ID_USUARIO
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
            TO_DATE(:hora_inicio, 'HH24:MI'),
            TO_DATE(:hora_fin, 'HH24:MI'),
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
            HORA_INICIO = TO_DATE(:hora_inicio, 'HH24:MI'),
            HORA_FIN = TO_DATE(:hora_fin, 'HH24:MI'),
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
