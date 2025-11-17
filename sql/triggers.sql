-------------------------------------------------------------
-- TRIGGERS DEL SISTEMA DE RESERVAS DE CITAS MÉDICAS
-- Oracle Database 21c / 18c
-- Autor: Fabrizio "Onichan"
-------------------------------------------------------------

-------------------------------------------------------------
-- 1) TRIGGER: VALIDAR QUE EL PACIENTE Y MÉDICO ESTÉN ACTIVOS
-------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_VALIDAR_USUARIOS_ACTIVOS
BEFORE INSERT ON CITA_MEDICA
FOR EACH ROW
DECLARE
    v_estado_paciente CHAR(1);
    v_estado_medico   CHAR(1);
BEGIN
    -----------------------------------------------------
    -- Validar paciente activo
    -----------------------------------------------------
    SELECT U.ESTADO_ACTIVO INTO v_estado_paciente
    FROM PACIENTE P
    JOIN USUARIO U ON U.ID_USUARIO = P.ID_USUARIO
    WHERE P.ID_PACIENTE = :NEW.ID_PACIENTE;

    IF v_estado_paciente = 'N' THEN
        RAISE_APPLICATION_ERROR(-20001, 'El paciente está inactivo.');
    END IF;

    -----------------------------------------------------
    -- Validar médico activo
    -----------------------------------------------------
    SELECT U.ESTADO_ACTIVO INTO v_estado_medico
    FROM HORARIO_MEDICO H
    JOIN MEDICO M ON M.ID_MEDICO = H.ID_MEDICO
    JOIN USUARIO U ON U.ID_USUARIO = M.ID_USUARIO
    WHERE H.ID_HORARIO = :NEW.ID_HORARIO;

    IF v_estado_medico = 'N' THEN
        RAISE_APPLICATION_ERROR(-20002, 'El médico está inactivo.');
    END IF;

END;
/
-------------------------------------------------------------
-- 2) TRIGGER: BLOQUEAR HORARIO YA RESERVADO O SIN CUPOS
-------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_BLOQUEAR_HORARIO
BEFORE INSERT ON CITA_MEDICA
FOR EACH ROW
DECLARE
    v_cupo_ocupado NUMBER;
    v_cupo_maximo  NUMBER;
BEGIN
    -----------------------------------------------------
    -- Validar si el horario está lleno
    -----------------------------------------------------
    SELECT CUPO_OCUPADO, CUPO_MAXIMO
    INTO v_cupo_ocupado, v_cupo_maximo
    FROM HORARIO_MEDICO
    WHERE ID_HORARIO = :NEW.ID_HORARIO;

    IF v_cupo_ocupado >= v_cupo_maximo THEN
        RAISE_APPLICATION_ERROR(-20003, 'El horario ya no tiene cupos disponibles.');
    END IF;

END;
/
-------------------------------------------------------------
-- 3) TRIGGER: ACTUALIZAR CUPOS - INSERT
-------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_ACTUALIZAR_CUPOS_INSERT
AFTER INSERT ON CITA_MEDICA
FOR EACH ROW
BEGIN
    UPDATE HORARIO_MEDICO
    SET CUPO_OCUPADO = CUPO_OCUPADO + 1
    WHERE ID_HORARIO = :NEW.ID_HORARIO;

    UPDATE HORARIO_MEDICO
    SET ESTADO_DISPONIBLE = 'N'
    WHERE ID_HORARIO = :NEW.ID_HORARIO
    AND CUPO_OCUPADO >= CUPO_MAXIMO;
END;
/
-------------------------------------------------------------
-- 4) TRIGGER: ACTUALIZAR CUPOS - DELETE
-------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_ACTUALIZAR_CUPOS_DELETE
AFTER DELETE ON CITA_MEDICA
FOR EACH ROW
BEGIN
    UPDATE HORARIO_MEDICO
    SET CUPO_OCUPADO = CUPO_OCUPADO - 1
    WHERE ID_HORARIO = :OLD.ID_HORARIO;

    UPDATE HORARIO_MEDICO
    SET ESTADO_DISPONIBLE = 'S'
    WHERE ID_HORARIO = :OLD.ID_HORARIO
    AND CUPO_OCUPADO < CUPO_MAXIMO;
END;
/
-------------------------------------------------------------
-- 5) TRIGGER: VALIDAR QUE EL PAGO EXISTA AL MARCAR "PAGADO"
-------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_VALIDAR_PAGO
BEFORE UPDATE OF ESTADO_PAGO ON CITA_MEDICA
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    IF :NEW.ESTADO_PAGO = 'PAGADO' THEN
        SELECT COUNT(*) INTO v_count
        FROM PAGO_CITA
        WHERE ID_CITA = :NEW.ID_CITA
        AND ESTADO_PAGO = 'REGISTRADO';

        IF v_count = 0 THEN
            RAISE_APPLICATION_ERROR(-20004,
                'No se puede marcar como PAGADO sin un pago registrado.');
        END IF;
    END IF;
END;
/
-------------------------------------------------------------
-- 6) TRIGGER DE AUDITORÍA (INSERT, UPDATE, DELETE)
-------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_AUDITORIA_CITAS
AFTER INSERT OR UPDATE OR DELETE ON CITA_MEDICA
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(20);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
    END IF;

    INSERT INTO AUDITORIA_CITA (
        ID_AUDITORIA,
        ID_CITA,
        OPERACION,
        USUARIO_ACCION,
        FECHA_HORA,
        VALOR_ANTERIOR,
        VALOR_NUEVO
    )
    VALUES (
        SEQ_AUDITORIA.NEXTVAL,
        CASE
            WHEN INSERTING THEN :NEW.ID_CITA
            WHEN UPDATING THEN :NEW.ID_CITA
            WHEN DELETING THEN :OLD.ID_CITA
        END,
        v_operacion,
        'APP_TKINTER',
        SYSDATE,
        CASE WHEN UPDATING OR DELETING THEN
            'Paciente:' || :OLD.ID_PACIENTE ||
            ', Horario:' || :OLD.ID_HORARIO ||
            ', Estado:' || :OLD.ESTADO_CITA ||
            ', Pago:' || :OLD.ESTADO_PAGO
        END,
        CASE WHEN INSERTING OR UPDATING THEN
            'Paciente:' || :NEW.ID_PACIENTE ||
            ', Horario:' || :NEW.ID_HORARIO ||
            ', Estado:' || :NEW.ESTADO_CITA ||
            ', Pago:' || :NEW.ESTADO_PAGO
        END
    );
END;
/
-------------------------------------------------------------
-- FIN DEL ARCHIVO
-- Sistema completo de triggers funcionando ✔
-------------------------------------------------------------
