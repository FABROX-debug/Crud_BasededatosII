# ui/pacientes_form.py - VERSIÓN MEJORADA
import tkinter as tk
from tkinter import ttk, messagebox
import re

from models.pacientes import listar_pacientes, crear_paciente, actualizar_paciente, eliminar_paciente
from utils.styles import BACKGROUND_COLOR

class PacientesForm(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=BACKGROUND_COLOR)
        self.master.configure(bg=BACKGROUND_COLOR)

        self.master.title("Gestión de Pacientes")
        self.master.geometry("1000x650")

        self.id_paciente_seleccionado = None

        self.crear_widgets()
        self.cargar_tabla()

    def crear_widgets(self):
        # Header
        header_frame = tk.Frame(self.master, bg=BACKGROUND_COLOR)
        header_frame.pack(fill="x", padx=20, pady=20)

        ttk.Label(
            header_frame, 
            text="Gestión de Pacientes",
            style="Title.TLabel"
        ).pack(side="left")

        # BUSCADOR
        search_frame = tk.Frame(header_frame, bg=BACKGROUND_COLOR)
        search_frame.pack(side="right")

        ttk.Label(search_frame, text="Buscar:", style="TLabel").pack(side="left", padx=5)
        
        self.txt_buscar = ttk.Entry(search_frame, width=30)
        self.txt_buscar.pack(side="left", padx=5)
        self.txt_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        # CONTENEDOR PRINCIPAL
        main_frame = tk.Frame(self.master, bg=BACKGROUND_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # FORMULARIO (IZQUIERDA)
        form_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=20)
        form_frame.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(form_frame, text="Datos del Paciente", font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w", pady=(0, 15))

        # Campos
        self.crear_campo(form_frame, "DNI", "txt_dni")
        self.crear_campo(form_frame, "Nombre Completo", "txt_nombre")
        self.crear_campo(form_frame, "Correo Electrónico", "txt_correo")
        self.crear_campo(form_frame, "Teléfono", "txt_telefono")

        # Botones de Acción
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(pady=20, fill="x")

        ttk.Button(btn_frame, text="Guardar", command=self.guardar, style="TButton").pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Nuevo / Limpiar", command=self.limpiar_form, style="Accent.TButton").pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar, style="Danger.TButton").pack(fill="x", pady=5)

        # TABLA (DERECHA)
        table_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=20)
        table_frame.pack(side="right", fill="both", expand=True)

        columnas = ("ID", "DNI", "Nombre", "Correo", "Telefono")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columnas,
            show="headings",
            style="Treeview"
        )

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("DNI", width=100)
        self.tree.column("Nombre", width=200)
        self.tree.column("Correo", width=200)
        self.tree.column("Telefono", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def crear_campo(self, parent, label, attr_name):
        ttk.Label(parent, text=label, background="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 2))
        entry = ttk.Entry(parent, width=35)
        entry.pack(fill="x", pady=(0, 10))
        setattr(self, attr_name, entry)

    def cargar_tabla(self):
        """Carga todos los pacientes"""
        self.lista_pacientes = listar_pacientes() # Guardar en memoria para filtrar
        self.actualizar_treeview(self.lista_pacientes)

    def actualizar_treeview(self, datos):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for p in datos:
            self.tree.insert("", tk.END, values=p)

    def filtrar_tabla(self, event):
        texto = self.txt_buscar.get().lower()
        if not texto:
            self.actualizar_treeview(self.lista_pacientes)
            return

        filtrados = []
        for p in self.lista_pacientes:
            # p[1] es DNI, p[2] es Nombre
            if texto in str(p[1]).lower() or texto in str(p[2]).lower():
                filtrados.append(p)
        
        self.actualizar_treeview(filtrados)

    def seleccionar_fila(self, event):
        try:
            item = self.tree.selection()[0]
            vals = self.tree.item(item, "values")
        except:
            return

        self.id_paciente_seleccionado = vals[0]

        # Rellenar formulario
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)

        self.txt_dni.insert(0, vals[1])
        self.txt_nombre.insert(0, vals[2])
        self.txt_correo.insert(0, vals[3])
        self.txt_telefono.insert(0, vals[4])

    def limpiar_form(self):
        self.id_paciente_seleccionado = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)
        self.txt_dni.focus()

    def validar_datos(self):
        dni = self.txt_dni.get().strip()
        nombre = self.txt_nombre.get().strip()
        correo = self.txt_correo.get().strip()
        telefono = self.txt_telefono.get().strip()

        if len(dni) != 8 or not dni.isdigit():
            messagebox.showwarning("Error", "El DNI debe tener exactamente 8 dígitos numéricos.")
            return False

        if nombre == "" or len(nombre) < 3:
            messagebox.showwarning("Error", "El nombre debe tener al menos 3 caracteres.")
            return False

        if correo != "":
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_email, correo):
                messagebox.showwarning("Error", "El correo electrónico no tiene un formato válido.")
                return False

        return True

    def guardar(self):
        if not self.validar_datos():
            return

        data = {
            "dni": self.txt_dni.get().strip(),
            "nombre": self.txt_nombre.get().strip(),
            "correo": self.txt_correo.get().strip(),
            "telefono": self.txt_telefono.get().strip()
        }

        try:
            if self.id_paciente_seleccionado is None:
                crear_paciente(data)
                messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            else:
                actualizar_paciente(self.id_paciente_seleccionado, data)
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")

            self.cargar_tabla()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el paciente:\n{e}")

    def eliminar(self):
        if self.id_paciente_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un paciente para eliminar.")
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de eliminar este paciente?\nEsta acción no se puede deshacer."
        )

        if not respuesta:
            return

        try:
            eliminar_paciente(self.id_paciente_seleccionado)
            messagebox.showinfo("Éxito", "Paciente eliminado correctamente.")
            self.cargar_tabla()
            self.limpiar_form()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el paciente:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PacientesForm(master=root)
    root.mainloop()