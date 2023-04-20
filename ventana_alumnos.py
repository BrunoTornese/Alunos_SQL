import tkinter as tk
from alumno import Alumno
from alumnos_manejos import AlumnoDAO

ventana_principal = tk.Tk()
ventana_principal.title("Sistema de Gestión de Alumnos")
tabla_frame = None # Variable global para la tabla

def mostrar_alumnos():
    global tabla_frame # Utilizar la variable global

    # Obtener la lista de alumnos de la base de datos
    alumnos = AlumnoDAO.seleccionar()

    # Borrar los widgets antiguos de la tabla si ya existe
    if tabla_frame is not None:
        tabla_frame.destroy()

    # Crear un nuevo frame para la tabla
    tabla_frame = tk.Frame(ventana_principal)
    tabla_frame.pack()

    # Crear la tabla de alumnos
    for i, alumno in enumerate(alumnos):
        etiqueta_nombre = tk.Label(tabla_frame, text=alumno.nombre)
        etiqueta_nombre.grid(row=i, column=0)

        etiqueta_apellido = tk.Label(tabla_frame, text=alumno.apellido)
        etiqueta_apellido.grid(row=i, column=1)

        etiqueta_id = tk.Label(tabla_frame, text=alumno.id)
        etiqueta_id.grid(row=i, column=2)

        boton_eliminar = tk.Button(tabla_frame, text="Eliminar", command=lambda alumno=alumno: Eliminar_Alumno(alumno))
        boton_eliminar.grid(row=i, column=3)

        # Crear el botón de actualizar alumno
        boton_actualizar = tk.Button(tabla_frame, text='Actualizar', command=lambda alumno=alumno: Alumno_Actualizar(alumno))
        boton_actualizar.grid(row=i, column=4)

    # Crear el botón para agregar un nuevo alumno
    boton_agregar_alumno = tk.Button(tabla_frame, text="Agregar", command=agregar_alumno)
    boton_agregar_alumno.grid(row=len(alumnos), column=0, pady=10, columnspan=5, sticky='we')



def agregar_alumno():
    # Crear la ventana para agregar un nuevo alumno
    ventana_agregar = tk.Toplevel(ventana_principal)
    ventana_agregar.title("Agregar alumno")

    # Crear los campos de texto y etiquetas para ingresar los datos del nuevo alumno
    etiqueta_nombre = tk.Label(ventana_agregar, text="Nombre:")
    etiqueta_nombre.pack()
    entrada_nombre = tk.Entry(ventana_agregar)
    entrada_nombre.pack()

    etiqueta_apellido = tk.Label(ventana_agregar, text="Apellido:")
    etiqueta_apellido.pack()
    entrada_apellido = tk.Entry(ventana_agregar)
    entrada_apellido.pack()

    # Función para agregar un nuevo alumno a la base de datos
    def agregar():
        # Obtener los datos ingresados en los campos de texto
        nombre = entrada_nombre.get()
        apellido = entrada_apellido.get()

        # Crear un objeto Alumno con los datos ingresados
        nuevo_alumno = Alumno(nombre=nombre, apellido=apellido)

        # Agregar el nuevo alumno a la base de datos
        AlumnoDAO.insertar(nuevo_alumno)

        # Cerrar la ventana de agregar alumno
        ventana_agregar.destroy()

        # Actualizar la tabla de alumnos
        mostrar_alumnos()

    # Crear el botón para agregar el alumno
    boton_agregar = tk.Button(ventana_agregar, text="Agregar", command=agregar)
    boton_agregar.pack()



def Eliminar_Alumno(alumno):
    # Crear la ventana para eliminar un nuevo alumno
    ventana_eliminar = tk.Toplevel(ventana_principal)
    ventana_eliminar.title("Eliminar alumno")

    # Crear los campos de texto y etiquetas para ingresar los datos del alumno
    etiqueta_id = tk.Label(ventana_eliminar, text="ID:")
    etiqueta_id.pack()
    entrada_id = tk.Entry(ventana_eliminar)
    entrada_id.pack()
    entrada_id.insert(tk.END, alumno.id)

    # Crear el botón para eliminar el alumno
    boton_eliminar = tk.Button(ventana_eliminar, text="Eliminar", command=lambda: eliminar_alumno(alumno, entrada_id.get(), ventana_eliminar))
    boton_eliminar.pack()

def eliminar_alumno(alumno, id_alumno, ventana_eliminar):
    # Eliminar el alumno
    AlumnoDAO.eliminar(alumno)

    ventana_eliminar.destroy()

    # Actualizar la tabla de alumnos
    mostrar_alumnos()

def Alumno_Actualizar(alumno):
    # Crear la ventana para actualizar los datos del alumno
    ventana_actualizar = tk.Toplevel(ventana_principal)
    ventana_actualizar.title("Actualizar alumno")

    # Crear los campos de texto y etiquetas para ingresar los nuevos datos del alumno
    etiqueta_nombre = tk.Label(ventana_actualizar, text="Nombre:")
    etiqueta_nombre.pack()
    entrada_nombre = tk.Entry(ventana_actualizar)
    entrada_nombre.insert(0, alumno.nombre)
    entrada_nombre.pack()

    etiqueta_apellido = tk.Label(ventana_actualizar, text="Apellido:")
    etiqueta_apellido.pack()
    entrada_apellido = tk.Entry(ventana_actualizar)
    entrada_apellido.insert(0, alumno.apellido)
    entrada_apellido.pack()

    etiqueta_id = tk.Label(ventana_actualizar, text="ID:")
    etiqueta_id.pack()
    entrada_id = tk.Entry(ventana_actualizar)
    entrada_id.insert(0, alumno.id)
    entrada_id.pack()

    # Función para actualizar los datos del alumno
    def actualizar_alumno():
        # Obtener los datos ingresados en los campos de texto
        nombre = entrada_nombre.get()
        apellido = entrada_apellido.get()
        id = entrada_id.get()

        # Crear un objeto Alumno con los datos ingresados
        alumno_actualizado = Alumno(id=id, nombre=nombre, apellido=apellido)

        # Actualizar los datos del alumno en la base de datos
        AlumnoDAO.actualizar(alumno_actualizado)

        # Actualizar la tabla de alumnos
        mostrar_alumnos()

        # Cerrar la ventana de actualizar alumno
        ventana_actualizar.destroy()

    # Crear el botón para actualizar el alumno
    boton_actualizar = tk.Button(ventana_actualizar, text="Actualizar", command=actualizar_alumno)
    boton_actualizar.pack()

    # Mostrar la ventana para actualizar los datos del alumno
    ventana_actualizar.mainloop()



# Iniciar el bucle de eventos de tkinter
ventana_principal.geometry('800x600')
mostrar_alumnos()
ventana_principal.mainloop()




