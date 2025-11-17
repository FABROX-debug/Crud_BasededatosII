# models/citas.py
# -----------------------------------------------------------
# CRUD COMPLETO DE CITA_MEDICA
# -----------------------------------------------------------

from db_oracle import fetch_all, execute_query


# -----------------------------------------------------------
# LISTAR CITAS
# -----------------------------------------------------------
def listar_citas():
    query = """
        SELECT C.ID_CITA,
               P.NOMBRE_COMPLETO AS PACIENTE,
               M.NOMBRE_COMPLETO AS MEDICO,
               E.NOMBRE_ESPECIALIDAD,
               H.FECHA,
               H.HORA_INICIO,
               C.ESTADO_CITA,
               C.ESTADO_PAGO
        FROM CITA_MEDICA C
        JOIN PACIENTE PA ON PA.ID_PACIENTE = C.ID_PACIENTE
        JOIN USUARIO P ON P.ID_USUARIO = PA.ID_USUARIO
        JOIN HORARIO_MEDICO H ON H.ID_HORARIO = C.ID_HORARIO
        JOIN MEDICO ME ON ME.ID_MEDICO = H.ID_MEDICO
        JOIN USUARIO M ON M.ID_USUARIO = ME.ID_USUARIO
        JOIN ESPECIALIDAD_MEDICA E ON E.ID_ESPECIALIDAD = ME.ID_ESPECIALIDAD
        ORDER BY H.FECHA, H.HORA_INICIO
    """
    return fetch_all(query)


# -----------------------------------------------------------
# INSERTAR CITA
# -----------------------------------------------------------
def crear_cita(data):
    query = """
        INSERT INTO CITA_MEDICA (
            ID_CITA,
            ID_PACIENTE,
            ID_HORARIO,
            ESTADO_CITA,
            ESTADO_PAGO,
            FECHA_RESERVA,
            MOTIVO,
            OBSERVACIONES
        )
        VALUES (
            SEQ_CITA.NEXTVAL,
            :id_paciente,
            :id_horario,
            :estado_cita,
            :estado_pago,
            SYSDATE,
            :motivo,
            :observaciones
        )
    """

    execute_query(query, data, commit=True)


# -----------------------------------------------------------
# ACTUALIZAR
# -----------------------------------------------------------
def actualizar_cita(id_cita, data):
    data["id_cita"] = id_cita
    query = """
        UPDATE CITA_MEDICA
        SET ID_PACIENTE = :id_paciente,
            ID_HORARIO = :id_horario,
            ESTADO_CITA = :estado_cita,
            ESTADO_PAGO = :estado_pago,
            MOTIVO = :motivo,
            OBSERVACIONES = :observaciones
        WHERE ID_CITA = :id_cita
    """
    execute_query(query, data, commit=True)


# -----------------------------------------------------------
# ELIMINAR
# -----------------------------------------------------------
def eliminar_cita(id_cita):
    query = "DELETE FROM CITA_MEDICA WHERE ID_CITA = :id"
    execute_query(query, {"id": id_cita}, commit=True)
