# models/pacientes.py
# ---------------------------------------------
# Funciones de consulta para PACIENTE
# ---------------------------------------------

from db_oracle import fetch_all

def listar_pacientes():
    """
    Retorna lista de pacientes:
    (ID_PACIENTE, NOMBRE_COMPLETO)
    """
    query = """
        SELECT P.ID_PACIENTE,
               U.NOMBRE_COMPLETO
        FROM PACIENTE P
        JOIN USUARIO U ON U.ID_USUARIO = P.ID_USUARIO
        WHERE U.TIPO_USUARIO = 'PACIENTE'
        ORDER BY U.NOMBRE_COMPLETO
    """
    return fetch_all(query)
