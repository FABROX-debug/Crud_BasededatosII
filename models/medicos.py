from db_oracle import fetch_all, execute_query


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
        INSERT INTO MEDICOS (
            ID_MEDICO, DNI, NOMBRE, ESPECIALIDAD, ESTADO
        ) VALUES (
            SEQ_MEDICOS.NEXTVAL,
            :dni,
            :nombre,
            :especialidad,
            :estado
        )
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
