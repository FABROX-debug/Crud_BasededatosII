# models/horarios.py
# ---------------------------------------------
# Funciones para HORARIO_MEDICO
# ---------------------------------------------

from db_oracle import fetch_all

def listar_horarios_disponibles(id_medico, fecha_str):
    """
    Retorna horarios disponibles para un médico y fecha dada.
    fecha_str debe venir en formato 'YYYY-MM-DD'.
    Devuelve: (ID_HORARIO, HORA_INICIO, HORA_FIN)
    """
    query = """
        SELECT H.ID_HORARIO,
               H.HORA_INICIO,
               H.HORA_FIN
        FROM HORARIO_MEDICO H
        WHERE H.ID_MEDICO = :id_medico
          AND H.FECHA = TO_DATE(:fecha, 'YYYY-MM-DD')
          AND H.ESTADO_DISPONIBLE = 'S'
        ORDER BY H.HORA_INICIO
    """
    params = {
        "id_medico": id_medico,
        "fecha": fecha_str
    }
    return fetch_all(query, params)
