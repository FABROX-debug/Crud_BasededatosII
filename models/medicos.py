# models/medicos.py
# ---------------------------------------------
# Funciones de consulta para MEDICO
# ---------------------------------------------

from db_oracle import fetch_all

def listar_medicos():
    """
    Retorna lista de médicos:
    (ID_MEDICO, NOMBRE_COMPLETO)
    """
    query = """
        SELECT M.ID_MEDICO,
               U.NOMBRE_COMPLETO
        FROM MEDICO M
        JOIN USUARIO U ON U.ID_USUARIO = M.ID_USUARIO
        WHERE U.TIPO_USUARIO = 'MEDICO'
        ORDER BY U.NOMBRE_COMPLETO
    """
    return fetch_all(query)
