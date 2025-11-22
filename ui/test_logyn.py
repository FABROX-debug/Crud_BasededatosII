# test_login.py - Script de diagnóstico para el sistema de login

from db_oracle import fetch_all

print("=" * 70)
print("DIAGNÓSTICO DEL SISTEMA DE LOGIN")
print("=" * 70)

# 1. Verificar todos los usuarios
print("\n1. USUARIOS EN LA BASE DE DATOS:")
try:
    usuarios = fetch_all("SELECT ID_USUARIO, DNI, NOMBRE, TIPO, PASSWORD, ESTADO FROM USUARIOS")
    print(f"✓ Total de usuarios: {len(usuarios)}\n")

    print(f"{'ID':<5} {'DNI':<12} {'NOMBRE':<30} {'TIPO':<10} {'PASSWORD':<20} {'ESTADO':<8}")
    print("-" * 90)

    for u in usuarios:
        print(f"{u[0]:<5} {u[1]:<12} {u[2]:<30} {u[3]:<10} {u[4]:<20} {u[5]:<8}")

except Exception as e:
    print(f"✗ ERROR: {e}")

# 2. Probar login con cada usuario
print("\n" + "=" * 70)
print("2. PRUEBA DE VALIDACIÓN DE USUARIOS:")
print("=" * 70)

test_usuarios = [
    ("12345678", "admin@citas.com"),
    ("97654321", "secret123"),
    ("55667788", "pediatra123"),
    ("99887766", "paciente1"),
]

for dni, password in test_usuarios:
    print(f"\n▶ Probando DNI: {dni} | Password: {password}")

    query = """
        SELECT ID_USUARIO, NOMBRE, TIPO
        FROM USUARIOS
        WHERE DNI = :dni
          AND PASSWORD = :password
          AND ESTADO = 'S'
    """

    try:
        resultado = fetch_all(query, {"dni": dni, "password": password})

        if resultado:
            print(f"  ✓ LOGIN EXITOSO")
            print(f"    - ID: {resultado[0][0]}")
            print(f"    - Nombre: {resultado[0][1]}")
            print(f"    - Tipo: {resultado[0][2]}")
        else:
            print(f"  ✗ LOGIN FALLIDO - No se encontró usuario o está inactivo")

            # Verificar si existe el usuario
            verif = fetch_all("SELECT ESTADO, PASSWORD FROM USUARIOS WHERE DNI = :dni", {"dni": dni})
            if verif:
                print(f"    - Usuario existe con estado: {verif[0][0]}")
                print(f"    - Password en BD: {verif[0][1]}")
                if verif[0][1] != password:
                    print(f"    - ⚠️ La contraseña NO coincide!")
            else:
                print(f"    - Usuario NO existe en la BD")

    except Exception as e:
        print(f"  ✗ ERROR: {e}")

# 3. Verificar usuarios activos
print("\n" + "=" * 70)
print("3. USUARIOS ACTIVOS (ESTADO = 'S'):")
print("=" * 70)

try:
    activos = fetch_all("""
        SELECT DNI, NOMBRE, TIPO, PASSWORD
        FROM USUARIOS
        WHERE ESTADO = 'S'
        ORDER BY TIPO, NOMBRE
    """)

    print(f"\n✓ Total de usuarios activos: {len(activos)}\n")

    for u in activos:
        print(f"  • {u[0]} - {u[1]} ({u[2]}) | Pass: {u[3]}")

except Exception as e:
    print(f"✗ ERROR: {e}")

print("\n" + "=" * 70)
print("FIN DEL DIAGNÓSTICO")
print("=" * 70)

print("\n📋 CREDENCIALES PARA PROBAR:")
print("-" * 50)
print("Admin Principal:")
print("  DNI: 12345678")
print("  Password: admin@citas.com")
print("\nSecretaria Central:")
print("  DNI: 97654321")
print("  Password: secret123")
print("\nDoctora Pediatra:")
print("  DNI: 55667788")
print("  Password: pediatra123")
print("-" * 50)