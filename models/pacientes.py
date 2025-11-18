from db_oracle import fetch_all, execute_query


def listar_pacientes():
    return fetch_all("""
        SELECT 
            ID_PACIENTE,
            DNI,
            NOMBRE
        FROM PACIENTES
        ORDER BY NOMBRE
    """)


def crear_paciente(data):
    query = """
        INSERT INTO PACIENTES (
            ID_PACIENTE, DNI, NOMBRE, CORREO, TELEFONO, FECHA_REG
        ) VALUES (
            SEQ_PACIENTES.NEXTVAL,
            :dni,
            :nombre,
            :correo,
            :telefono,
            SYSDATE
        )
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
