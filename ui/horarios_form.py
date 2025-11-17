# ui/horarios_form.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.horarios import listar_horarios, crear_horario, actualizar_horario, eliminar_horario
from models.medicos import listar_medicos

class HorariosForm(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Gestión de Horarios")
        self.master.geometry("750x550")

        self.id_horario = None

        self.crear_widgets()
        self.cargar_medicos()
        self.cargar_tabla()

    # ----------------------------------------------------------------------
    def crear_widgets(self):
        tk.Label(self.master, text="Gestión de Horarios",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        form = tk.Frame(self.master)
        form.pack(pady=10)

        # Labels
        tk.Label(form, text="Médico:").grid(row=0, column=0, pady=5)
        tk.Label(form, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, pady=5)
        tk.Label(form, text="Hora inicio:").grid(row=2, column=0, pady=5)
        tk.Label(form, text="Hora fin:").grid(row=3, column=0, pady=5)
        tk.Label(form, text="Disponible:").grid(row=4, column=0, pady=5)

        # Campos
        self.cbo_medico = ttk.Combobox(form, width=30, state="readonly")
        self.txt_fecha = tk.Entry(form, width=20)
        self.txt_hora_inicio = tk.Entry(form, width=20)
        self.txt_hora_fin = tk.Entry(form, width=20)
        self.cbo_disponible = ttk.Combobox(form, values=["S", "N"], width=5)

        self.cbo_medico.grid(row=0, column=1)
        self.txt_fecha.grid(row=1, column=1)
        self.txt_hora_inicio.grid(row=2, column=1)
        self.txt_hora_fin.grid(row=3, column=1)
        self.cbo_disponible.grid(row=4, column=1)

        # BOTONES
        btns = tk.Frame(self.master)
        btns.pack(pady=10)

        tk.Button(btns, text="Nuevo", width=12, command=self.limpiar_form).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Guardar", width=12, command=self.guardar).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)

        # TABLA
        self.tree = ttk.Treeview(
            self.master,
            columns=("ID", "Médico", "Fecha", "Inicio", "Fin", "Disp"),
            show="headings",
            height=12
        )

        headers = ["ID", "Médico", "Fecha", "Inicio", "Fin", "Disponible"]
        for i, col in enumerate(headers):
            self.tree.heading(i, text=col)

        self.tree.column(0, width=60)
        self.tree.column(1, width=180)
        self.tree.column(2, width=100)
        self.tree.column(3, width=70)
        self.tree.column(4, width=70)
        self.tree.column(5, width=90)

        self.tree.pack(fill="x", pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    # ----------------------------------------------------------------------
    def cargar_medicos(self):
        medicos = listar_medicos()
        nombres = [f"{m[0]} - {m[2] if len(m) > 2 else m[1]}" for m in medicos]
        self.cbo_medico["values"] = nombres

    # ----------------------------------------------------------------------
    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for h in listar_horarios():
            self.tree.insert("", tk.END, values=h)

    # ----------------------------------------------------------------------
    def seleccionar(self, event):
        item = self.tree.selection()[0]
        vals = self.tree.item(item, "values")

        self.id_horario = vals[0]

        self.cbo_medico.set(vals[1])
        self.txt_fecha.delete(0, tk.END)
        self.txt_hora_inicio.delete(0, tk.END)
        self.txt_hora_fin.delete(0, tk.END)
        self.cbo_disponible.set(vals[5])

        self.txt_fecha.insert(0, vals[2])
        self.txt_hora_inicio.insert(0, vals[3])
        self.txt_hora_fin.insert(0, vals[4])

    # ----------------------------------------------------------------------
    def limpiar_form(self):
        self.id_horario = None
        self.cbo_medico.set("")
        self.txt_fecha.delete(0, tk.END)
        self.txt_hora_inicio.delete(0, tk.END)
        self.txt_hora_fin.delete(0, tk.END)
        self.cbo_disponible.set("")

    # ----------------------------------------------------------------------
    def guardar(self):
        try:
            medico_id = int(self.cbo_medico.get().split(" - ")[0])
        except:
            messagebox.showerror("Error", "Seleccione un médico válido.")
            return

        data = {
            "id_medico": medico_id,
            "fecha": self.txt_fecha.get().strip(),
            "hora_inicio": self.txt_hora_inicio.get().strip(),
            "hora_fin": self.txt_hora_fin.get().strip(),
            "disponible": self.cbo_disponible.get().strip() or "S"
        }

        if self.id_horario is None:
            crear_horario(data)
            messagebox.showinfo("OK", "Horario registrado.")
        else:
            actualizar_horario(self.id_horario, data)
            messagebox.showinfo("OK", "Horario actualizado.")

        self.cargar_tabla()
        self.limpiar_form()

    # ----------------------------------------------------------------------
    def eliminar(self):
        if self.id_horario is None:
            messagebox.showwarning("Aviso", "Seleccione un horario.")
            return

        eliminar_horario(self.id_horario)
        messagebox.showinfo("OK", "Horario eliminado.")

        self.cargar_tabla()
        self.limpiar_form()


# Para testear solo este archivo
if __name__ == "__main__":
    root = tk.Tk()
    app = HorariosForm(master=root)
    app.mainloop()
