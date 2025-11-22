# models/usuarios.py - VERSIÓN CORREGIDA FINAL
from db_oracle import fetch_all, execute_query


def listar_usuarios():
    """Lista todos los usuarios del sistema"""
    return fetch_all("""
        SELECT ID_USUARIO, DNI, NOMBRE, TIPO, ESTADO
        FROM USUARIOS
        ORDER BY NOMBRE
    """)


def validar_usuario(dni, password):
    """
    Valida las credenciales de un usuario.

    Busca un usuario activo (ESTADO='S') que coincida con el DNI y PASSWORD.

    Args:
        dni: DNI del usuario (8 dígitos)
        password: Contraseña ingresada por el usuario

    Returns:
        Lista con tupla (ID_USUARIO, NOMBRE, TIPO) si es válido
        Lista vacía si las credenciales son incorrectas
    """
    query = """
        SELECT ID_USUARIO, NOMBRE, TIPO
        FROM USUARIOS
        WHERE TRIM(DNI) = TRIM(:dni)
          AND TRIM(PASSWORD) = TRIM(:password)
          AND ESTADO = 'S'
    """

    try:
        resultado = fetch_all(query, {"dni": dni, "password": password})
        return resultado if resultado else []
    except Exception as e:
        print(f"ERROR en validar_usuario: {e}")
        raise e


def obtener_usuario_por_dni(dni):
    """
    Obtiene información de un usuario por su DNI (sin validar password).
    Útil para verificar si el usuario existe.

    Args:
        dni: DNI del usuario

    Returns:
        Lista con datos del usuario si existe
    """
    query = """
        SELECT ID_USUARIO, DNI, NOMBRE, TIPO, PASSWORD, ESTADO
        FROM USUARIOS
        WHERE TRIM(DNI) = TRIM(:dni)
    """
    return fetch_all(query, {"dni": dni})


def crear_usuario(data):
    """
    Crea un nuevo usuario en el sistema.

    Args:
        data: Diccionario con las claves: dni, nombre, tipo, password, estado
    """
    query = """
        INSERT INTO USUARIOS (DNI, NOMBRE, TIPO, PASSWORD, ESTADO)
        VALUES (:dni, :nombre, :tipo, :password, :estado)
    """
    execute_query(query, data, commit=True)


def actualizar_usuario(id_usuario, data):
    """
    Actualiza los datos de un usuario existente.

    Args:
        id_usuario: ID del usuario a actualizar
        data: Diccionario con las claves: dni, nombre, tipo, password, estado
    """
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


def eliminar_usuario(id_usuario):
    """
    Elimina un usuario del sistema.

    Args:
        id_usuario: ID del usuario a eliminar
    """
    execute_query(
        "DELETE FROM USUARIOS WHERE ID_USUARIO = :id",
        {"id": id_usuario},
        commit=True
    )


def cambiar_password(id_usuario, nueva_password):
    """
    Cambia la contraseña de un usuario.

    Args:
        id_usuario: ID del usuario
        nueva_password: Nueva contraseña
    """
    query = """
        UPDATE USUARIOS
        SET PASSWORD = :password
        WHERE ID_USUARIO = :id
    """
    execute_query(query, {
        "id": id_usuario,
        "password": nueva_password
    }, commit=True)


def verificar_dni_existe(dni, excluir_id=None):
    """
    Verifica si un DNI ya existe en la base de datos.

    Args:
        dni: DNI a verificar
        excluir_id: ID de usuario a excluir de la búsqueda (útil para edición)

    Returns:
        True si el DNI existe, False si no
    """
    if excluir_id:
        query = """
            SELECT COUNT(*) FROM USUARIOS 
            WHERE DNI = :dni AND ID_USUARIO != :id
        """
        resultado = fetch_all(query, {"dni": dni, "id": excluir_id})
    else:
        query = "SELECT COUNT(*) FROM USUARIOS WHERE DNI = :dni"
        resultado = fetch_all(query, {"dni": dni})

    return resultado[0][0] > 0 if resultado else False