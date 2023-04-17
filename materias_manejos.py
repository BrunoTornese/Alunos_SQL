from cursor import Cursor  # Se importa la clase Cursor desde el módulo cursor
from conexion import logging  # Se importa el objeto logging desde el módulo conexion
from materia import Materia  # Se importa la clase Materia desde el módulo materia

_AGREGAR = "INSERT INTO materia (nombre_materia) VALUES (%s)"  # Consulta SQL para agregar una materia
_SELECCIONAR = "SELECT id_materia, nombre_materia FROM materia"  # Consulta SQL para seleccionar todas las materias
_CAMBIAR = "UPDATE materia SET nombre_materia = %s WHERE id_materia = %s"  # Consulta SQL para actualizar una materia
_ELIMINAR = "DELETE FROM materia WHERE id_materia = %s"  # Consulta SQL para eliminar una materia

class MateriaDAO:
    # Función para agregar una materia a la base de datos
    @classmethod
    def crear_materia(cls, materia):
        with Cursor() as cursor:
            logging.debug(f'Agregando una materia')  # Se registra un mensaje de debug
            valores = (materia.nombre,)  # Se crea una tupla con los valores a insertar en la consulta SQL
            cursor.execute(_AGREGAR, valores)  # Se ejecuta la consulta SQL
            logging.debug(f'Materia agregada {materia}')  # Se registra un mensaje de debug
            return cursor.rowcount  # Se retorna la cantidad de filas afectadas por la consulta SQL

    # Función para leer todas las materias de la base de datos
    @classmethod
    def leer_materias(cls):
        with Cursor() as cursor:
            cursor.execute(_SELECCIONAR)  # Se ejecuta la consulta SQL
            registros = cursor.fetchall()  # Se obtienen todos los registros devueltos por la consulta SQL
            materias = []  # Se crea una lista vacía para almacenar las materias
            for registro in registros:
                # Se crea un objeto de la clase Materia con los datos del registro y se agrega a la lista
                materia = Materia(registro[0], registro[1])
                materias.append(materia)
            return materias  # Se retorna la lista de materias

    # Función para imprimir en pantalla todas las materias de la base de datos
    @classmethod
    def listar_materias(cls):
        materias = MateriaDAO.leer_materias()  # Se obtienen todas las materias de la base de datos
        for materia in materias:
            print(f"{materia.id_materia}: {materia.nombre}")  # Se imprime en pantalla el ID y el nombre de cada materia

    # Función para actualizar una materia en la base de datos
    @classmethod
    def actualizar_materia(cls, materia):
        with Cursor() as cursor:
            valores = (materia.nombre, materia.id_materia)  # Se crea una tupla con los valores a actualizar en la consulta SQL
            cursor.execute(_CAMBIAR, valores)  # Se ejecuta la consulta SQL
            logging.debug(f'Materia actualizada: {materia}')  # Se registra un mensaje de debug
            return cursor.rowcount  # Se retorna la cantidad de filas afectadas por la consulta SQL

    # Función para eliminar una materia
    def eliminar_materia(cls, materia):
        with Cursor() as cursor:
            # Crear una tupla con el id de la materia a eliminar
            valores = (materia.id_materia,)
            # Ejecutar la consulta de eliminación utilizando la tupla de valores
            cursor.execute(_ELIMINAR, valores)
            # Devolver el número de filas afectadas por la eliminación
            return cursor.rowcount


if __name__ == '__main__':
    materias = MateriaDAO.leer_materias()
    for materia in materias:
        logging.debug(materia.nombre)

    #materia = Materia(1, 'Matematicas avanzadas')
   # materia_agregada = MateriaDAO.crear_materia(materia)
    #logging.debug(f'Matera agregada: {materia_agregada}')

    #materia = Materia(5, 'Matematicas intermedia')
    #materia_actualizar = MateriaDAO.actualizar_materia(materia)
    #logging.debug(f'Materia actualizada: {materia_actualizar}')

    #materia = Materia(nombre='Matematicas intermedias')
    #materia_eliminada = MateriaDAO.eliminar_materia(materia)
    #ogging.debug(f'Alumno eliminado {materia_eliminada}')
            
