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


# =====================================================
# models/medicos.py - CORREGIDO PARA IDENTITY
# =====================================================

def listar_medicos():
    return fetch_all("""
        SELECT 
            ID_MEDICO,
            DNI,
            NOMBRE,
            ESPECIALIDAD,
            ESTADO
        FROM MEDICOS
        ORDER BY NOMBRE
    """)


def crear_medico(data):
    query = """
        INSERT INTO MEDICOS (DNI, NOMBRE, ESPECIALIDAD, ESTADO)
        VALUES (:dni, :nombre, :especialidad, :estado)
    """
    execute_query(query, data, commit=True)


def actualizar_medico(id_medico, data):
    data["id"] = id_medico
    query = """
        UPDATE MEDICOS
        SET DNI = :dni,
            NOMBRE = :nombre,
            ESPECIALIDAD = :especialidad,
            ESTADO = :estado
        WHERE ID_MEDICO = :id
    """
    execute_query(query, data, commit=True)


def eliminar_medico(id_medico):
    execute_query(
        "DELETE FROM MEDICOS WHERE ID_MEDICO = :id",
        {"id": id_medico},
        commit=True
    )