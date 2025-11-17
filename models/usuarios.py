# models/usuarios.py
# -----------------------------------------------------------
# CRUD de USUARIOS basado en la estructura real de tu BD
# -----------------------------------------------------------

from db_oracle import fetch_all, execute_query

# -----------------------------------------------------------
# LISTAR USUARIOS
# -----------------------------------------------------------
def listar_usuarios():
    query = """
        SELECT ID_USUARIO, DNI, NOMBRE, TIPO, ESTADO
        FROM USUARIOS
        ORDER BY NOMBRE
    """
    return fetch_all(query)


# -----------------------------------------------------------
# BUSCAR USUARIO POR DNI Y PASSWORD (LOGIN)
# -----------------------------------------------------------
def validar_usuario(dni, password):
    query = """
        SELECT ID_USUARIO, NOMBRE, TIPO
        FROM USUARIOS
        WHERE DNI = :dni
          AND PASSWORD = :password
          AND ESTADO = 'S'
    """
    return fetch_all(query, {"dni": dni, "password": password})


# -----------------------------------------------------------
# INSERTAR USUARIO
# -----------------------------------------------------------
def crear_usuario(data):
    query = """
        INSERT INTO USUARIOS (
            ID_USUARIO,
            DNI,
            NOMBRE,
            TIPO,
            PASSWORD,
            ESTADO
        )
        VALUES (
            SEQ_USUARIOS.NEXTVAL,
            :dni,
            :nombre,
            :tipo,
            :password,
            :estado
        )
    """
    execute_query(query, data, commit=True)


# -----------------------------------------------------------
# ACTUALIZAR USUARIO
# -----------------------------------------------------------
def actualizar_usuario(id_usuario, data):
    data["id_usuario"] = id_usuario
    query = """
        UPDATE USUARIOS
        SET DNI = :dni,
            NOMBRE = :nombre,
            TIPO = :tipo,
            PASSWORD = :password,
            ESTADO = :estado
        WHERE ID_USUARIO = :id_usuario
    """
    execute_query(query, data, commit=True)


# -----------------------------------------------------------
# ELIMINAR USUARIO
# -----------------------------------------------------------
def eliminar_usuario(id_usuario):
    execute_query(
        "DELETE FROM USUARIOS WHERE ID_USUARIO = :id",
        {"id": id_usuario},
        commit=True
    )
