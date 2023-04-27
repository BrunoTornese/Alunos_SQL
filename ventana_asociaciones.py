import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from alumno import Alumno
from alumno_materiaDAO import Alumno_MateriaDAO
from alumnos_manejos import AlumnoDAO
from conexion import logging
from materia import Materia

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Asociaciones de Alumnos y Materias")
        self.geometry("800x600")
        # inicializar la lista de asociaciones como una lista vacía
        self.lista_asociaciones = [] 

        # Crear un menú con diferentes opciones
        menu_bar = tk.Menu(self)
        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Salir", command=self.quit)
        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        self.config(menu=menu_bar)

        # Crear un frame para mostrar los alumnos y sus materias asociadas
        self.frame_alumnos = tk.Frame(self)
        self.frame_alumnos.pack(pady=20)

        # Crear un botón para ver todas las asociaciones de un alumno
        boton_ver_asociaciones = tk.Button(self, text="Ver Asociaciones", command=self.mostrar_asociaciones)
        boton_ver_asociaciones.pack(pady=20)

        # Crear un botón para buscar las asociaciones de un alumno por ID
        boton_buscar_asociaciones = tk.Button(self, text="Buscar Alumnos", command=self.abrir_formulario_busqueda)
        boton_buscar_asociaciones.pack(pady=20)

        # Crear un frame para agregar asociaciones de alumnos y materias
        self.frame_agregar = tk.Frame(self)
        self.frame_agregar.pack(pady=20)

        # Crear un botón para agregar la asociación
        boton_agregar_asociaciones = tk.Button(self, text="Agregar Asociaciones", command=self.abrir_formulario_agregar)
        boton_agregar_asociaciones.pack(pady=20)

    def mostrar_asociaciones(self):
        dao = Alumno_MateriaDAO()
        asociaciones = dao.ver_asociaciones()
        # Limpiar el frame de alumnos antes de agregar los nuevos datos
        for widget in self.frame_alumnos.winfo_children():
            widget.destroy()
        # Iterar sobre el diccionario de alumnos y materias, y agregar un Label para cada alumno
        for id_alumno, datos_alumno in asociaciones.items():
            nombre_alumno = datos_alumno['nombre_alumno']
            materias = datos_alumno['materias']
            label_alumno = tk.Label(self.frame_alumnos, text=f"Alumno: {nombre_alumno}")
            label_alumno.pack()
            text_materias = tk.Text(self.frame_alumnos, height=len(materias), width=50)
            text_materias.pack()
            # Agregar cada materia asociada al Text
            for materia in materias:
                text_materias.insert(tk.END, f"- {materia['nombre_materia']}\n")
    
    # Funcion para crear el formulario de busqueda
    def abrir_formulario_busqueda(self): 
        # Crear una ventana para buscar las asociaciones de un alumno por ID, nombre y apellido
        ventana_busqueda = tk.Toplevel(self)
        ventana_busqueda.title("Buscar Asociaciones de un Alumno")
        ventana_busqueda.geometry("300x150")
        # Crear una entrada para ingresar el ID del alumno a buscar
        label_id_alumno = tk.Label(ventana_busqueda, text="ID del alumno:")
        label_id_alumno.pack()
        id_alumno_entry = tk.Entry(ventana_busqueda)
        id_alumno_entry.pack()
        # Crear una entrada para ingresar el nombre del alumno a buscar
        label_nombre_alumno = tk.Label(ventana_busqueda, text="Nombre del alumno:")
        label_nombre_alumno.pack()
        nombre_alumno_entry = tk.Entry(ventana_busqueda)
        nombre_alumno_entry.pack()
        # Crear una entrada para ingresar el apellido del alumno a buscar
        label_apellido_alumno = tk.Label(ventana_busqueda, text="Apellido del alumno:")
        label_apellido_alumno.pack()
        apellido_alumno_entry = tk.Entry(ventana_busqueda)
        apellido_alumno_entry.pack()
        # Crear un botón para buscar al alumno
        boton_buscar = tk.Button(ventana_busqueda, text="Buscar", command=lambda: self.buscar_alumno((id_alumno_entry.get(), nombre_alumno_entry.get(), apellido_alumno_entry.get())))
        boton_buscar.pack()
    #Funcion para buscar un alumno en la bd

    def buscar_alumno(self, datos_busqueda):
        id_alumno_str, nombre_alumno, apellido_alumno = datos_busqueda
        # Convertir el ID del alumno a entero
        id_alumno = int(id_alumno_str)
        if self.lista_asociaciones is None:
            messagebox.showerror("Error", "La lista de asociaciones no ha sido inicializada.")
            return
        # Obtener las asociaciones del alumno desde la base de datos
        asociaciones = self.mostrar_asociaciones_alumno(id_alumno, nombre_alumno, apellido_alumno)
        # Mostrar las asociaciones en la lista
        if self.lista_asociaciones is not None:
            self.lista_asociaciones.delete(0, tk.END)
            for asociacion in asociaciones:
                self.lista_asociaciones.insert(tk.END, asociacion)
        else:
            messagebox.showerror("Error", "La lista de asociaciones no ha sido inicializada.")
    
    #Funcion para mostrar las asociaciones
    def mostrar_asociaciones_alumno(self, id_alumno, nombre_alumno, apellido_alumno):
        # Verificar si se ingresó el nombre y/o apellido del alumno
        if nombre_alumno or apellido_alumno:
            # Obtener todos los alumnos y filtrar por nombre y/o apellido
            alumnos = AlumnoDAO.seleccionar()
            alumnos_filtrados = []
            for alumno in alumnos:
                if nombre_alumno and nombre_alumno.lower() not in alumno.nombre.lower():
                    continue
                if apellido_alumno and apellido_alumno.lower() not in alumno.apellido.lower():
                    continue
                alumnos_filtrados.append(alumno)
            # Si no se encontraron alumnos, mostrar un mensaje de advertencia
            if not alumnos_filtrados:
                messagebox.showwarning("Sin Alumnos", "No se encontraron alumnos que coincidan con los criterios de búsqueda.")
                return []
            # Si se encontraron múltiples alumnos, mostrar un mensaje de advertencia
            if len(alumnos_filtrados) > 1:
                messagebox.showwarning("Múltiples Alumnos", "Se encontraron múltiples alumnos que coinciden con los criterios de búsqueda. Por favor, especifique el ID del alumno.")
                return []
            # Si se encontró un solo alumno, usar su ID para buscar las asociaciones
            alumno = alumnos_filtrados[0]
            asociaciones = Alumno_MateriaDAO.seleccionar_por_alumno(alumno)
        else:
            # Si no se ingresó el nombre ni el apellido del alumno, buscar por ID
            alumno = Alumno(id_alumno)
            asociaciones = Alumno_MateriaDAO.seleccionar_por_alumno(alumno)
        # Verificar si se encontraron asociaciones
        if not asociaciones:
            messagebox.showwarning("Sin Asociaciones", "No se encontraron asociaciones para el alumno seleccionado.")
            return []
        return asociaciones
    
    # Funcion para crear el formulario de agregar
    def abrir_formulario_agregar(self):
        # Crear una ventana para agregar una asociacion
        ventana_agregar = tk.Toplevel(self)
        ventana_agregar.title("Agregar Asociación")
        ventana_agregar.geometry("300x200")
        
        # Crear una entrada para ingresar el ID del alumno
        label_id_alumno = tk.Label(ventana_agregar, text="ID del alumno:")
        label_id_alumno.pack()
        self.id_alumno_entry = tk.Entry(ventana_agregar)
        self.id_alumno_entry.pack()
        
        # Crear una entrada para ingresar el ID de la materia
        label_id_materia = tk.Label(ventana_agregar, text="ID de la materia:")
        label_id_materia.pack()
        self.id_materia_entry = tk.Entry(ventana_agregar)
        self.id_materia_entry.pack()
        
        # Crear un botón para agregar la asociación
        boton_agregar = tk.Button(ventana_agregar, text="Agregar", command=self.agregar_asociacion)
        boton_agregar.pack(pady=10)

    # Funcion para agregar asociacion entre alumno y materia
    def agregar_asociacion(self):
        # Obtener los datos de la ventana
        id_alumno = int(self.id_alumno_entry.get())
        id_materia = int(self.id_materia_entry.get())
        # Crear una instancia de Alumno_MateriaDAO
        dao = Alumno_MateriaDAO()
        # Llamar a la función agregar de Alumno_MateriaDAO
        dao.agregar(id_alumno, id_materia)
        # Cerrar la ventana
        self.ventana.destroy()

if __name__ == "__main__":
    ventana = VentanaPrincipal()
    ventana.mainloop()
