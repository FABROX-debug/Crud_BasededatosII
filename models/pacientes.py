# =====================================================
# models/pacientes.py - CORREGIDO PARA IDENTITY
# =====================================================
from db_oracle import fetch_all, execute_query


def listar_pacientes():
    return fetch_all("""
        SELECT 
            ID_PACIENTE,
            DNI,
            NOMBRE,
            NVL(CORREO, '') AS CORREO,
            NVL(TELEFONO, '') AS TELEFONO
        FROM PACIENTES
        ORDER BY NOMBRE
    """)


def crear_paciente(data):
    query = """
        INSERT INTO PACIENTES (DNI, NOMBRE, CORREO, TELEFONO)
        VALUES (:dni, :nombre, :correo, :telefono)
    """
    execute_query(query, data, commit=True)


def actualizar_paciente(id_paciente, data):
    data["id"] = id_paciente
    query = """
        UPDATE PACIENTES
        SET DNI = :dni,
            NOMBRE = :nombre,
            CORREO = :correo,
            TELEFONO = :telefono
        WHERE ID_PACIENTE = :id
    """
    execute_query(query, data, commit=True)


def eliminar_paciente(id_paciente):
    execute_query(
        "DELETE FROM PACIENTES WHERE ID_PACIENTE = :id",
        {"id": id_paciente},
        commit=True
    )