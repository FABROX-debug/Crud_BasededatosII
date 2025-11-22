# ui/medicos_form.py - VERSIÓN MEJORADA
import tkinter as tk
from tkinter import ttk, messagebox

from models.medicos import listar_medicos, crear_medico, actualizar_medico, eliminar_medico
from models.horarios import listar_horarios_por_medico
from utils.styles import BACKGROUND_COLOR

class MedicosForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=BACKGROUND_COLOR)
        self.master.configure(bg=BACKGROUND_COLOR)

        self.master.title("Gestión de Médicos")
        self.master.geometry("1100x700")

        self.id_medico = None

        self.crear_widgets()
        self.cargar_tabla_medicos()

    def crear_widgets(self):
        # Header
        header_frame = tk.Frame(self.master, bg=BACKGROUND_COLOR)
        header_frame.pack(fill="x", padx=20, pady=20)

        ttk.Label(
            header_frame,
            text="Gestión de Médicos",
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

        # IZQUIERDA: FORMULARIO Y TABLA MÉDICOS
        left_panel = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # FORMULARIO
        form_frame = ttk.Frame(left_panel, style="Card.TFrame", padding=20)
        form_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(form_frame, text="Datos del Médico", font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w", pady=(0, 15))

        # Grid layout para formulario
        grid_frame = tk.Frame(form_frame, bg="white")
        grid_frame.pack(fill="x")

        self.crear_campo_grid(grid_frame, "DNI", "txt_dni", 0, 0)
        self.crear_campo_grid(grid_frame, "Nombre", "txt_nombre", 0, 1)
        self.crear_campo_grid(grid_frame, "Especialidad", "txt_especialidad", 1, 0)
        
        # Estado (Combobox) - con contenedor
        estado_frame = tk.Frame(grid_frame, bg="white")
        estado_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nw")
        
        ttk.Label(estado_frame, text="Estado", background="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 5))
        self.cbo_estado = ttk.Combobox(estado_frame, values=["S", "N"], state="readonly", width=26)
        self.cbo_estado.pack(anchor="w", fill="x")

        # Botones
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(pady=10, fill="x")

        ttk.Button(btn_frame, text="Guardar", command=self.guardar, style="TButton").pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(btn_frame, text="Nuevo", command=self.limpiar_form, style="Accent.TButton").pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar, style="Danger.TButton").pack(side="left", fill="x", expand=True, padx=2)

        # TABLA MÉDICOS
        table_frame = ttk.Frame(left_panel, style="Card.TFrame", padding=20)
        table_frame.pack(fill="both", expand=True)

        self.tree_medicos = ttk.Treeview(
            table_frame,
            columns=("ID", "DNI", "Nombre", "Especialidad", "Estado"),
            show="headings",
            height=8,
            style="Treeview"
        )

        headers = ["ID", "DNI", "Nombre", "Especialidad", "Estado"]
        widths = [50, 100, 180, 150, 60]

        for i, col in enumerate(headers):
            self.tree_medicos.heading(col, text=col)
            self.tree_medicos.column(col, width=widths[i])

        # Scrollbar
        scrollbar_med = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_medicos.yview)
        self.tree_medicos.configure(yscroll=scrollbar_med.set)

        self.tree_medicos.pack(side="left", fill="both", expand=True)
        scrollbar_med.pack(side="right", fill="y")
        
        self.tree_medicos.bind("<<TreeviewSelect>>", self.seleccionar_medico)

        # DERECHA: HORARIOS
        right_panel = ttk.Frame(main_frame, style="Card.TFrame", padding=20)
        right_panel.pack(side="right", fill="both", padx=(10, 0))

        ttk.Label(right_panel, text="Horarios Asignados", font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w", pady=(0, 15))

        self.tree_horarios = ttk.Treeview(
            right_panel,
            columns=("Fecha", "Inicio", "Fin"),
            show="headings",
            height=15,
            style="Treeview"
        )

        self.tree_horarios.heading("Fecha", text="Fecha")
        self.tree_horarios.heading("Inicio", text="Inicio")
        self.tree_horarios.heading("Fin", text="Fin")

        self.tree_horarios.column("Fecha", width=100)
        self.tree_horarios.column("Inicio", width=80)
        self.tree_horarios.column("Fin", width=80)

        self.tree_horarios.pack(fill="both", expand=True, pady=(0, 10))

        ttk.Button(
            right_panel,
            text="🔄 Actualizar Horarios",
            command=self.cargar_horarios_medico,
            style="TButton"
        ).pack(fill="x")

    def crear_campo_grid(self, parent, label, attr_name, row, col):
        # Contenedor para el campo (Label + Entry)
        field_frame = tk.Frame(parent, bg="white")
        field_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nw")
        
        ttk.Label(field_frame, text=label, background="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 5))
        
        entry = ttk.Entry(field_frame, width=28)
        entry.pack(anchor="w", fill="x")
        setattr(self, attr_name, entry)

    def cargar_tabla_medicos(self):
        """Carga todos los médicos en la tabla"""
        try:
            self.lista_medicos = listar_medicos()
            print(f"DEBUG: Medicos cargados: {len(self.lista_medicos)}")
            for m in self.lista_medicos:
                print(f"DEBUG: Medico: {m}")
            self.actualizar_treeview(self.lista_medicos)
        except Exception as e:
            print(f"DEBUG: Error cargando medicos: {e}")
            messagebox.showerror("Error", f"Error cargando médicos: {e}")

    def actualizar_treeview(self, datos):
        for item in self.tree_medicos.get_children():
            self.tree_medicos.delete(item)
        
        for m in datos:
            self.tree_medicos.insert("", tk.END, values=m)

    def filtrar_tabla(self, event):
        texto = self.txt_buscar.get().lower()
        if not texto:
            self.actualizar_treeview(self.lista_medicos)
            return

        filtrados = []
        for m in self.lista_medicos:
            # m[1] es DNI, m[2] es Nombre, m[3] es Especialidad
            if (texto in str(m[1]).lower() or 
                texto in str(m[2]).lower() or 
                texto in str(m[3]).lower()):
                filtrados.append(m)
        
        self.actualizar_treeview(filtrados)

    def seleccionar_medico(self, event):
        try:
            item = self.tree_medicos.selection()[0]
            vals = self.tree_medicos.item(item, "values")
        except:
            return

        self.id_medico = vals[0]

        # Llenar formulario
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_especialidad.delete(0, tk.END)

        self.txt_dni.insert(0, vals[1])
        self.txt_nombre.insert(0, vals[2])
        self.txt_especialidad.insert(0, vals[3])
        self.cbo_estado.set(vals[4])

        # Cargar horarios del médico
        self.cargar_horarios_medico()

    def cargar_horarios_medico(self):
        # Limpiar tabla
        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

        if not self.id_medico:
            return

        try:
            horarios = listar_horarios_por_medico(int(self.id_medico))
            
            # Insertar horarios en la tabla (filtrando columnas relevantes)
            for h in horarios:
                # h = (ID, Fecha, Inicio, Fin, Disponible)
                self.tree_horarios.insert("", tk.END, values=(h[1], h[2], h[3]))

        except Exception as e:
            print(f"Error al cargar horarios: {e}")

    def limpiar_form(self):
        self.id_medico = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_especialidad.delete(0, tk.END)
        self.cbo_estado.set("")

        for item in self.tree_horarios.get_children():
            self.tree_horarios.delete(item)

    def validar_datos(self):
        dni = self.txt_dni.get().strip()
        nombre = self.txt_nombre.get().strip()
        especialidad = self.txt_especialidad.get().strip()
        estado = self.cbo_estado.get()

        if len(dni) != 8 or not dni.isdigit():
            messagebox.showwarning("Error", "El DNI debe tener 8 dígitos.")
            return False

        if nombre == "" or len(nombre) < 3:
            messagebox.showwarning("Error", "El nombre debe tener al menos 3 caracteres.")
            return False

        if especialidad == "" or len(especialidad) < 3:
            messagebox.showwarning("Error", "La especialidad debe tener al menos 3 caracteres.")
            return False

        if estado not in ["S", "N"]:
            messagebox.showwarning("Error", "Debe seleccionar un estado válido (S/N).")
            return False

        return True

    def guardar(self):
        if not self.validar_datos():
            return

        data = {
            "dni": self.txt_dni.get().strip(),
            "nombre": self.txt_nombre.get().strip(),
            "especialidad": self.txt_especialidad.get().strip(),
            "estado": self.cbo_estado.get().strip()
        }

        try:
            if self.id_medico is None:
                crear_medico(data)
                messagebox.showinfo("Éxito", "Médico registrado correctamente.")
            else:
                actualizar_medico(self.id_medico, data)
                messagebox.showinfo("Éxito", "Médico actualizado correctamente.")

            self.cargar_tabla_medicos()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def eliminar(self):
        if self.id_medico is None:
            messagebox.showwarning("Aviso", "Seleccione un médico.")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de eliminar este médico?\n\n"
            "⚠️ ADVERTENCIA: También se eliminarán sus horarios y citas asociadas.\n"
            "Esta acción no se puede deshacer."
        )

        if not respuesta:
            return

        try:
            eliminar_medico(self.id_medico)
            messagebox.showinfo("Éxito", "Médico eliminado correctamente.")
            self.cargar_tabla_medicos()
            self.limpiar_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicosForm(master=root)
    app.mainloop()