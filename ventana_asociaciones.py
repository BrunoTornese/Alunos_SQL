import tkinter as tk
from tkinter import messagebox
from alumno import Alumno
from alumno_materiaDAO import Alumno_MateriaDAO
from alumnos_manejos import AlumnoDAO
from materias_manejos import MateriaDAO
from conexion import logging

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        # Creacion del titulo geometry de ventana texto asociaciones y lista asociaciones
        self.title("Asociaciones de Alumnos y Materias")
        self.geometry("800x600")
        self.texto_asociaciones = tk.Text(self, height=10, width=50)
        self.lista_asociaciones = tk.Listbox(self, height=10)
        self.lista_asociaciones.pack()
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
        # Crear un boton para buscar asociaciones de una materia 
        boton_buscar_asociaciones_materia = tk.Button(self, text="Buscar Materia", command=self.abrir_formulario_busqueda_materia)
        boton_buscar_asociaciones_materia.pack(pady=20)
        # Crear un frame para agregar asociaciones de alumnos y materias
        self.frame_agregar = tk.Frame(self)
        self.frame_agregar.pack(pady=20)
        # Crear un botón para agregar la asociación
        boton_agregar_asociaciones = tk.Button(self, text="Agregar Asociaciones", command=self.abrir_formulario_agregar)
        boton_agregar_asociaciones.pack(pady=20)
        #Crear un boton para eliminar asociacion
        boton_eliminar_asociacion = tk.Button(self, text="Eliminar Asociación", command=self.abrir_formulario_eliminar_asociacion)
        boton_eliminar_asociacion.pack(pady=10)
    
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

    def abrir_formulario_busqueda(self):
        # Crear una ventana para buscar un alumno
        ventana_buscar_Alumno = tk.Toplevel(self)
        ventana_buscar_Alumno.title("Buscar Alumno")
        ventana_buscar_Alumno.geometry("400x200")
        # Crear una entrada para ingresar el ID 
        label_id_Alumno = tk.Label(ventana_buscar_Alumno, text="ID Del Alumno:")
        label_id_Alumno.pack()        
        self.id_Alumno_entry = tk.Entry(ventana_buscar_Alumno)
        self.id_Alumno_entry.pack()
        # Crear una entrada para ingresar el nombre
        label_Nombre_Alumno = tk.Label(ventana_buscar_Alumno, text="Nombre Del Alumno:")
        label_Nombre_Alumno.pack()
        self.nombre_alumno_entry = tk.Entry(ventana_buscar_Alumno)
        self.nombre_alumno_entry.pack()
        # Crear una entrada para ingresar el apellido
        label_Apellido_Alumno = tk.Label(ventana_buscar_Alumno, text="Apellido Del Alumno:")
        label_Apellido_Alumno.pack()
        self.apellido_alumno_entry = tk.Entry(ventana_buscar_Alumno)
        self.apellido_alumno_entry.pack()
        # Crear un botón para buscar el alumno
        boton_buscar = tk.Button(ventana_buscar_Alumno, text="Buscar", command=self.buscar_asociacion)
        boton_buscar.pack(pady=10)


    def buscar_asociacion(self):
        id_Alumno = self.id_Alumno_entry.get()
        if not id_Alumno:
            messagebox.showerror("Error", "El campo de ID de la asociación no puede estar vacío")
            return
        # Buscar el alumno en la base de datos
        alumno = AlumnoDAO.obtener_alumno(id_Alumno)
        logging.debug(f'Buscando asociaciones del alumno {alumno}')
        if alumno is None:
            messagebox.showerror("Error", "El alumno ingresado no se encuentra en la base de datos")
            return
        # Mostrar las asociaciones correspondientes al alumno en pantalla
        self.actualizar_lista(alumno)

    def actualizar_lista(self, alumno):
        # Obtener las asociaciones del alumno de la base de datos
        asociaciones = Alumno_MateriaDAO.seleccionar_por_alumno(alumno)
        logging.debug(f'Asociaciones: {asociaciones}')
        # Limpiar la lista de asociaciones en la ventana principal
        self.lista_asociaciones.delete(0, tk.END)
        # Agregar las asociaciones del alumno a la lista
        for asociacion in asociaciones:
            nombre_materia = asociacion["materia"].nombre
            self.lista_asociaciones.insert(tk.END, nombre_materia)

    def abrir_formulario_agregar(self):
        # Crear una ventana para agregar una asociacion
        ventana_agregar = tk.Toplevel(self)
        ventana_agregar.title("Agregar Asociación")
        ventana_agregar.geometry("400x350")
        # Crear una entrada para ingresar el ID del alumno
        label_id_alumno = tk.Label(ventana_agregar, text="ID del alumno:")
        label_id_alumno.pack()
        self.id_alumno_entry = tk.Entry(ventana_agregar)
        self.id_alumno_entry.pack()
        # Crear una entrada para ingresar el nombre del alumno
        label_nombre_alumno = tk.Label(ventana_agregar, text="Nombre del alumno:")
        label_nombre_alumno.pack()
        self.nombre_alumno_entry = tk.Entry(ventana_agregar)
        self.nombre_alumno_entry.pack()
        # Crear una entrada para ingresar el apellido del alumno
        label_apellido_alumno = tk.Label(ventana_agregar, text="Apellido del alumno:")
        label_apellido_alumno.pack()
        self.apellido_alumno_entry = tk.Entry(ventana_agregar)
        self.apellido_alumno_entry.pack()
        # Crear una entrada para ingresar el ID de la materia
        label_id_materia = tk.Label(ventana_agregar, text="ID de la materia:")
        label_id_materia.pack()
        self.id_materia_entry = tk.Entry(ventana_agregar)
        self.id_materia_entry.pack()
        # Crear un botón para agregar la asociación
        boton_agregar = tk.Button(ventana_agregar, text="Agregar", command=self.agregar_asociacion_materia)
        boton_agregar.pack(pady=10)

    def agregar_asociacion(self):
        id_alumno = self.id_alumno_entry.get()
        id_materia = self.id_materia_entry.get()
        if not id_alumno or not id_materia:
            messagebox.showerror("Error", "Los campos de ID del alumno y materia no pueden estar vacíos")
            return
        # Convertir a enteros
        id_alumno = int(id_alumno)
        id_materia = int(id_materia)
        # Verificar que existan los IDs en las tablas de Alumno y Materia
        alumno = AlumnoDAO.obtener_alumno(id_alumno)
        materia = MateriaDAO.obtener_materia(id_materia)
        if alumno is None:
            messagebox.showerror("Error", f"No se encontró ningún alumno con ID {id_alumno}")
            return
        if materia is None:
            messagebox.showerror("Error", f"No se encontró ninguna materia con ID {id_materia}")
            return
        # Llamar a la función agregar de Alumno_MateriaDAO, pasándole los IDs
        filas_afectadas = Alumno_MateriaDAO.agregar(id_alumno, id_materia)
        if filas_afectadas == 1:
            messagebox.showinfo("Éxito", f"La asociación entre Alumno con ID {id_alumno} y Materia con ID {id_materia} se ha agregado correctamente")
            self.id_alumno_entry.delete(0, tk.END)
            self.id_materia_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Hubo un problema al agregar la asociación")
    
    def abrir_formulario_busqueda_materia(self):
        # Crear una ventana para buscar un Materia
        ventana_buscar_Materia = tk.Toplevel(self)
        ventana_buscar_Materia.title("Buscar Materia")
        ventana_buscar_Materia.geometry("400x200")
        # Crear una entrada para ingresar el ID 
        label_id_Materia = tk.Label(ventana_buscar_Materia, text="ID De la Materia:")
        label_id_Materia.pack()        
        self.id_Materia_entry = tk.Entry(ventana_buscar_Materia)
        self.id_Materia_entry.pack()
        # Crear una entrada para ingresar el nombre
        label_Nombre_Materia = tk.Label(ventana_buscar_Materia, text="Nombre Del Materia:")
        label_Nombre_Materia.pack()
        self.nombre_Materia_entry = tk.Entry(ventana_buscar_Materia)
        self.nombre_Materia_entry.pack()
        # Crear un botón para buscar el Materia
        boton_buscar = tk.Button(ventana_buscar_Materia, text="Buscar", command=self.buscar_asociacion_materia)
        boton_buscar.pack(pady=10)

    def buscar_asociacion_materia(self):
        id_Materia = self.id_Materia_entry.get()
        if not id_Materia:
            messagebox.showerror("Error", "El campo de ID de la asociación no puede estar vacío")
            return
        # Buscar la materia en la base de datos
        materia = MateriaDAO.obtener_materia(id_Materia)
        logging.debug(f'Buscando asociaciones de la Materia {materia}')
        if materia is None:
            messagebox.showerror("Error", "La Materia ingresado no se encuentra en la base de datos")
            return
        # Mostrar las asociaciones correspondientes a la materia en pantalla
        self.actualizar_lista_materia(materia)

    def actualizar_lista_materia(self, materia):
        # Limpiar la lista de asociaciones previas
        self.lista_asociaciones.delete(0, tk.END)
        # Obtener las asociaciones de alumnos que estén relacionados con la materia
        asociaciones = Alumno_MateriaDAO.seleccionar_por_materia(materia)
        # Mostrar las asociaciones en la lista
        for asociacion in asociaciones:
            alumno_nombre = f"{asociacion['alumno'].nombre} {asociacion['alumno'].apellido}"
            materia_nombre = asociacion['materia'].nombre
            self.lista_asociaciones.insert(tk.END, f"{alumno_nombre} - {materia_nombre}")
    
    def abrir_formulario_eliminar_asociacion(self):
        # Crear una ventana para eliminar la asociación de materia y alumno
        ventana_eliminar_asociacion = tk.Toplevel(self)
        ventana_eliminar_asociacion.title("Eliminar Asociación")
        ventana_eliminar_asociacion.geometry("400x200")
        # Crear una entrada para ingresar el nombre del alumno
        label_nombre_alumno = tk.Label(ventana_eliminar_asociacion, text="Nombre del Alumno:")
        label_nombre_alumno.pack()
        self.nombre_alumno_entry = tk.Entry(ventana_eliminar_asociacion)
        self.nombre_alumno_entry.pack()
        # Crear una entrada para ingresar el apellido del alumno
        label_apellido_alumno = tk.Label(ventana_eliminar_asociacion, text="Apellido del Alumno:")
        label_apellido_alumno.pack()
        self.apellido_alumno_entry = tk.Entry(ventana_eliminar_asociacion)
        self.apellido_alumno_entry.pack()
        # Crear una entrada para ingresar el nombre de la materia
        label_nombre_materia = tk.Label(ventana_eliminar_asociacion, text="Nombre de la Materia:")
        label_nombre_materia.pack()
        self.nombre_materia_entry = tk.Entry(ventana_eliminar_asociacion)
        self.nombre_materia_entry.pack()
        # Crear un botón para eliminar la asociación de materia y alumno
        boton_eliminar = tk.Button(ventana_eliminar_asociacion, text="Eliminar", command=self.eliminar_asociacion_materia_alumno)
        boton_eliminar.pack(pady=10)

    def eliminar_asociacion_materia_alumno(self):
        nombre_alumno = self.nombre_alumno_entry.get()
        apellido_alumno = self.apellido_alumno_entry.get()
        nombre_materia = self.nombre_materia_entry.get()
        logging.debug(f'nombre_alumno: {nombre_alumno}, apellido_alumno: {apellido_alumno}, nombre_materia: {nombre_materia}')
        if not nombre_alumno or not apellido_alumno or not nombre_materia:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos")
            return
        # Buscar el alumno en la base de datos
        alumno_id = AlumnoDAO.obtener_id_alumno(nombre_alumno, apellido_alumno)
        alumno = Alumno(nombre_alumno, apellido_alumno, alumno_id)
        if alumno is None:
            messagebox.showerror("Error", "El alumno ingresado no se encuentra en la base de datos")
            return
        # Buscar la materia en la base de datos
        materia = MateriaDAO.obtener_id_materia(nombre_materia)
        if materia is None:
            messagebox.showerror("Error", "La materia ingresada no se encuentra en la base de datos")
            return
        # Eliminar la asociación de materia y alumno
        filas_afectadas = Alumno_MateriaDAO.eliminar_asociacion(nombre_alumno, apellido_alumno, nombre_materia)
        logging.debug(f'Filas afectadas: {filas_afectadas}')
        if filas_afectadas == 0:
            messagebox.showerror("Error", "La asociación que intenta eliminar no existe")
            return
        messagebox.showinfo("Información", "La asociación ha sido eliminada correctamente")

if __name__ == "__main__":
    ventana = VentanaPrincipal()
    ventana.mainloop()
