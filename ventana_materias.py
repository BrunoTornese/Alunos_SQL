import tkinter as tk
from materia import Materia
from materias_manejos import MateriaDAO

ventana_principal = tk.Tk()
ventana_principal.title("Sistema de Gestión de Materias")
tabla_frame = None # Variable global para la tabla

def mostrar_materias():
    global tabla_frame # Utilizar la variable global

    # Obtener la lista de materias de la base de datos
    materias = MateriaDAO.leer_materias()

    # Borrar los widgets antiguos de la tabla si ya existe
    if tabla_frame is not None:
        tabla_frame.destroy()

    # Crear un nuevo frame para la tabla
    tabla_frame = tk.Frame(ventana_principal)
    tabla_frame.pack()

    # Crear la tabla de materias
    for i, materia in enumerate(materias):
        etiqueta_nombre = tk.Label(tabla_frame, text=materia.nombre)
        etiqueta_nombre.grid(row=i, column=0)

        etiqueta_id = tk.Label(tabla_frame, text=materia.id_materia)
        etiqueta_id.grid(row=i, column=1)

        boton_eliminar = tk.Button(tabla_frame, text="Eliminar", command=lambda materia=materia: Eliminar_Materia(materia))
        boton_eliminar.grid(row=i, column=3)

        # Crear el botón de actualizar materia
        boton_actualizar = tk.Button(tabla_frame, text='Actualizar', command=lambda materia=materia: Materia_Actualizar(materia))
        boton_actualizar.grid(row=i, column=4)

    # Crear el botón para agregar un nuevo materia
    boton_agregar_materia = tk.Button(tabla_frame, text="Agregar", command=agregar_materia)
    boton_agregar_materia.grid(row=len(materias), column=0, pady=10, columnspan=5, sticky='we')

def agregar_materia():
    # Crear la ventana para agregar un nuevo materia
    ventana_agregar = tk.Toplevel(ventana_principal)
    ventana_agregar.title("Agregar Materia")

    # Crear los campos de texto y etiquetas para ingresar los datos del nuevo materia
    etiqueta_nombre = tk.Label(ventana_agregar, text="Nombre:")
    etiqueta_nombre.pack()
    entrada_nombre = tk.Entry(ventana_agregar)
    entrada_nombre.pack()

    # Función para agregar un nuevo materia a la base de datos
    def agregar():
        # Obtener los datos ingresados en los campos de texto
        nombre = entrada_nombre.get()

        # Crear un objeto materia con los datos ingresados
        nueva_materia = Materia(nombre=nombre,)

        # Agregar el nuevo materia a la base de datos
        MateriaDAO.crear_materia(nueva_materia)

        # Cerrar la ventana de agregar materia
        ventana_agregar.destroy()

        # Actualizar la tabla de materia
        mostrar_materias()

    # Crear el botón para agregar el materia
    boton_agregar = tk.Button(ventana_agregar, text="Agregar Materia", command=agregar)
    boton_agregar.pack()

def Eliminar_Materia(materia):
    # Crear la ventana para eliminar una materia
    ventana_eliminar = tk.Toplevel(ventana_principal)
    ventana_eliminar.title("Eliminar Materia")

    # Crear los campos de texto y etiquetas para ingresar los datos del materia
    etiqueta_id = tk.Label(ventana_eliminar, text="ID:")
    etiqueta_id.pack()
    entrada_id = tk.Entry(ventana_eliminar)
    entrada_id.pack()
    entrada_id.insert(tk.END, materia.id_materia)

    # Crear el botón para eliminar el materia
    boton_eliminar = tk.Button(ventana_eliminar, text="Eliminar", command=lambda: eliminar_materia(materia, entrada_id.get(), ventana_eliminar))
    boton_eliminar.pack()

def eliminar_materia(materia, id_materia, ventana_eliminar):
    # Eliminar el materia
    MateriaDAO.eliminar_materia(materia)

    ventana_eliminar.destroy()

    # Actualizar la tabla de materias
    mostrar_materias()

def Materia_Actualizar(materia):
    # Crear la ventana para actualizar los datos de la materia
    ventana_actualizar = tk.Toplevel(ventana_principal)
    ventana_actualizar.title("Actualizar Materia")

    # Crear los campos de texto y etiquetas para ingresar los nuevos datos de la materia
    etiqueta_nombre = tk.Label(ventana_actualizar, text="Nombre:")
    etiqueta_nombre.pack()
    entrada_nombre = tk.Entry(ventana_actualizar)
    entrada_nombre.insert(0, materia.nombre)
    entrada_nombre.pack()

    etiqueta_id = tk.Label(ventana_actualizar, text="ID:")
    etiqueta_id.pack()
    entrada_id = tk.Entry(ventana_actualizar)
    entrada_id.insert(0, materia.id_materia)
    entrada_id.pack()

    # Función para actualizar los datos de la materia
    def actualizar_materia():
        # Obtener los datos ingresados en los campos de texto
        nombre = entrada_nombre.get()
        id_materia = entrada_id.get()

        # Crear un objeto materia con los datos ingresados
        materia_actualizada = Materia(id_materia=id_materia, nombre=nombre)

        # Actualizar los datos de la materia en la base de datos
        MateriaDAO.actualizar_materia(materia_actualizada)

        # Actualizar la tabla de materias
        mostrar_materias()

        # Cerrar la ventana de actualizar materia
        ventana_actualizar.destroy()

    # Crear el botón para actualizar la materia
    boton_actualizar = tk.Button(ventana_actualizar, text="Actualizar", command=actualizar_materia)
    boton_actualizar.pack()

    # Mostrar la ventana para actualizar los datos de la materia
    ventana_actualizar.mainloop()



# Iniciar el bucle de eventos de tkinter
if __name__ == '__main__':
    ventana_principal.geometry('800x600')
    mostrar_materias()
    ventana_principal.mainloop()
