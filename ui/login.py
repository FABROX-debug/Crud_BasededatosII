# ui/login.py - VERSIÓN CORREGIDA FINAL
import tkinter as tk
from tkinter import ttk, messagebox

from models.usuarios import validar_usuario, obtener_usuario_por_dni
from utils.styles import apply_styles, BACKGROUND_COLOR, PRIMARY_COLOR

USUARIO_LOGEADO = None


class LoginWindow(tk.Frame):

    def __init__(self, master=None, on_login_success=None):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success

        self.master.title("Iniciar Sesión - Sistema Citas Médicas")
        self.master.resizable(False, False)

        # Tamaño ventana
        self.ancho = 400
        self.alto = 450
        self.centrar_ventana()

        apply_styles(self.master)
        self.crear_widgets()

    def centrar_ventana(self):
        self.master.update_idletasks()
        w, h = self.ancho, self.alto
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.master.geometry(f"{w}x{h}+{x}+{y}")

    def crear_widgets(self):
        cont = tk.Frame(self.master, padx=0, pady=0, bg=BACKGROUND_COLOR)
        cont.pack(expand=True, fill="both")

        # Contenedor central centrado
        center_frame = tk.Frame(cont, bg=BACKGROUND_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        ttk.Label(
            center_frame,
            text="Sistema de Citas Médicas",
            style="Title.TLabel"
        ).pack(pady=(0, 5))

        ttk.Label(
            center_frame,
            text="Bienvenido de nuevo",
            style="Subtitle.TLabel"
        ).pack(pady=(0, 20))

        # Card principal
        card = ttk.Frame(center_frame, padding=30, style="Card.TFrame")
        card.pack(fill="both", expand=True)

        # DNI
        ttk.Label(
            card,
            text="DNI",
            background="white",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.txt_usuario = ttk.Entry(card, width=35, font=("Segoe UI", 10))
        self.txt_usuario.pack(fill="x", pady=(0, 15))
        self.txt_usuario.focus()

        # Contraseña
        ttk.Label(
            card,
            text="Contraseña",
            background="white",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.txt_password = ttk.Entry(card, width=35, show="●", font=("Segoe UI", 10))
        self.txt_password.pack(fill="x", pady=(0, 20))

        # Press Enter para login
        self.txt_usuario.bind("<Return>", lambda e: self.txt_password.focus())
        self.txt_password.bind("<Return>", lambda e: self.validar_login())

        # Botón de login
        btn_login = ttk.Button(
            card,
            text="INICIAR SESIÓN",
            width=25,
            command=self.validar_login,
            style="TButton"
        )
        btn_login.pack(pady=(10, 0), fill="x")

        # Footer
        tk.Label(
            center_frame,
            text="© 2023 Sistema Médico v2.0",
            font=("Segoe UI", 8),
            fg="gray",
            bg=BACKGROUND_COLOR,
        ).pack(pady=(20, 0))

    def validar_login(self):
        """Valida las credenciales del usuario"""
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()

        # Validación de campos vacíos
        if usuario == "" or password == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor complete todos los campos."
            )
            return

        # Validación de formato de DNI
        if not usuario.isdigit() or len(usuario) != 8:
            messagebox.showwarning(
                "DNI inválido",
                "El DNI debe contener exactamente 8 dígitos numéricos."
            )
            self.txt_usuario.focus()
            return

        # Intentar validar usuario
        try:
            resultado = validar_usuario(usuario, password)

            # Si no hay resultados, verificar si el usuario existe
            if not resultado or len(resultado) == 0:
                # Verificar si el DNI existe en la base de datos
                usuario_existe = obtener_usuario_por_dni(usuario)

                if usuario_existe and len(usuario_existe) > 0:
                    estado = usuario_existe[0][5]  # Campo ESTADO

                    if estado == 'N':
                        messagebox.showerror(
                            "Usuario inactivo",
                            "Su usuario está inactivo.\n\n"
                            "Contacte al administrador del sistema."
                        )
                    else:
                        messagebox.showerror(
                            "Contraseña incorrecta",
                            "La contraseña ingresada es incorrecta.\n\n"
                            "Verifique e intente nuevamente."
                        )

                    # Limpiar solo el campo de contraseña
                    self.txt_password.delete(0, tk.END)
                    self.txt_password.focus()
                else:
                    messagebox.showerror(
                        "Usuario no encontrado",
                        f"No existe un usuario con DNI: {usuario}\n\n"
                        "Verifique el DNI ingresado."
                    )
                    self.txt_usuario.focus()

                return

            # Login exitoso - extraer datos
            user_id, nombre, tipo = resultado[0]

            # Guardar usuario logueado globalmente
            global USUARIO_LOGEADO
            USUARIO_LOGEADO = {
                "id": user_id,
                "nombre": nombre,
                "tipo": tipo,
                "dni": usuario
            }

            # Mensaje de bienvenida
            rol_texto = {
                "ADMIN": "Administrador",
                "MEDICO": "Médico",
                "PACIENTE": "Paciente"
            }.get(tipo, "Usuario")

            messagebox.showinfo(
                "¡Bienvenido!",
                f"Acceso concedido\n\n"
                f"Usuario: {nombre}\n"
                f"Rol: {rol_texto}"
            )

            # Cerrar ventana de login
            self.master.destroy()

            # Redirigir al menú principal
            if self.on_login_success:
                self.on_login_success()

        except Exception as e:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar a la base de datos:\n\n{str(e)}\n\n"
                f"Verifique su conexión e intente nuevamente."
            )
            print(f"ERROR DETALLADO: {e}")


def get_usuario_logueado():
    """Retorna el usuario actualmente logueado"""
    return USUARIO_LOGEADO


# Para pruebas independientes
if __name__ == "__main__":
    root = tk.Tk()


    def test_success():
        print("=" * 50)
        print("LOGIN EXITOSO")
        print("=" * 50)
        print(f"Usuario logueado: {USUARIO_LOGEADO}")
        print("=" * 50)


    app = LoginWindow(master=root, on_login_success=test_success)
    root.mainloop()