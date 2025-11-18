# models/horarios.py
from db_oracle import fetch_all, execute_query

# -----------------------------
# LISTAR HORARIOS DISPONIBLES
# -----------------------------
def listar_horarios_disponibles(id_medico, fecha_str, horario_actual=None):
    """
    Devuelve horarios disponibles para un médico y fecha determinados.
    Si se está editando una cita, se puede pasar horario_actual para incluirlo
    aunque ya esté reservado.
    """
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
    horarios = fetch_all(query, {
        "id_medico": id_medico,
        "fecha": fecha_str
    })

    # Si se está editando y el horario actual no está libre, lo agregamos
    if horario_actual:
        existe = any(h[0] == horario_actual for h in horarios)
        if not existe:
            actual = obtener_horario_por_id(horario_actual)
            if actual and actual[1] == id_medico and actual[2] == fecha_str:
                horarios.append((actual[0], actual[2], actual[3], actual[4]))

    return horarios


# -----------------------------
# LISTAR FECHAS DISPONIBLES POR MÉDICO
# -----------------------------
def listar_fechas_disponibles(id_medico, horario_actual=None):
    """
    Retorna las fechas en las que el médico tiene horarios disponibles.
    Si se está editando una cita, se incluye la fecha del horario_actual
    aunque esté reservada.
    """
    query = """
        SELECT DISTINCT TO_CHAR(FECHA, 'YYYY-MM-DD') AS FECHA
        FROM HORARIOS
        WHERE ID_MEDICO = :id_medico
          AND DISPONIBLE = 'S'
          AND ID_HORARIO NOT IN (
                SELECT ID_HORARIO FROM CITAS
          )
        ORDER BY FECHA
    """
    fechas = [f[0] for f in fetch_all(query, {"id_medico": id_medico})]

    if horario_actual:
        actual = obtener_horario_por_id(horario_actual)
        if actual and actual[1] == id_medico and actual[2] not in fechas:
            fechas.append(actual[2])

    return fechas


# -----------------------------
# OBTENER HORARIO POR ID (UTILIDAD)
# -----------------------------
def obtener_horario_por_id(id_horario):
    """Devuelve (id_horario, id_medico, fecha_str, inicio, fin, disponible)."""
    query = """
        SELECT ID_HORARIO,
               ID_MEDICO,
               TO_CHAR(FECHA, 'YYYY-MM-DD') AS FECHA,
               HORA_INICIO,
               HORA_FIN,
               DISPONIBLE
        FROM HORARIOS
        WHERE ID_HORARIO = :id
    """
    rows = fetch_all(query, {"id": id_horario})
    return rows[0] if rows else None


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
