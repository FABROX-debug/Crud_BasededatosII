import os

# Estructura de carpetas
folders = [
    "models",
    "ui",
    "utils",
    "sql"
]

# Archivos vacíos por carpeta
files = {
    "": ["main.py", "db_config.py", "db_oracle.py"],
    "models": ["__init__.py", "citas.py", "pacientes.py", "medicos.py", "horarios.py"],
    "ui": ["__init__.py", "dashboard.py", "citas_form.py", "pacientes_form.py", "medicos_form.py"],
    "utils": ["__init__.py", "validators.py", "styles.py"],
    "sql": ["schema.sql", "triggers.sql"]
}

# Crear carpetas y archivos
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Carpeta creada: {folder}")

# Crear archivos
for folder, file_list in files.items():
    for file_name in file_list:
        path = os.path.join(folder, file_name) if folder != "" else file_name
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("")  # archivo vacío
            print(f"Archivo creado: {path}")

print("\nEstructura de proyecto creada exitosamente 🎉")
