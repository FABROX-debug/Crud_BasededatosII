from db_oracle import get_connection

conn = get_connection()

if conn:
    print("Conexión exitosa a Oracle!")
else:
    print("Fallo en la conexión")
