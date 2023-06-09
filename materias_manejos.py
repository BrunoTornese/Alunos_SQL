from cursor import Cursor  # Se importa la clase Cursor desde el módulo cursor
from conexion import logging  # Se importa el objeto logging desde el módulo conexion
from materia import Materia  # Se importa la clase Materia desde el módulo materia

_AGREGAR = "INSERT INTO materia (nombre_materia) VALUES (%s)"  # Consulta SQL para agregar una materia
_SELECCIONAR = "SELECT id_materia, nombre_materia FROM materia"  # Consulta SQL para seleccionar todas las materias
_CAMBIAR = "UPDATE materia SET nombre_materia = %s WHERE id_materia = %s"  # Consulta SQL para actualizar una materia
_ELIMINAR = "DELETE FROM materia WHERE id_materia = %s"  # Consulta SQL para eliminar una materia

class MateriaDAO:
    _SELECCIONAR_MATERIA = "SELECT id_materia FROM materia WHERE nombre_materia = %s"
    _SELECCIONAR_MATERIA_POR_ID = 'SELECT id_materia, nombre_materia FROM materia WHERE id_materia = %s'

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
    @classmethod
    def eliminar_materia(cls, materia):
        with Cursor() as cursor:
            # Crear una tupla con el id de la materia a eliminar
            valores = (materia.id_materia,)
            # Ejecutar la consulta de eliminación utilizando la tupla de valores
            cursor.execute(_ELIMINAR, valores)
            # Devolver el número de filas afectadas por la eliminación
            return cursor.rowcount
        
    @classmethod
    def obtener_id_materia(cls, nombre_materia): # Seleccionamos el id de la materia por su nombre
        with Cursor() as cursor:
            valores = (nombre_materia,)
            cursor.execute(cls._SELECCIONAR_MATERIA, valores)
            resultado = cursor.fetchone() # Recuperamos la primera fila de resultados
            if resultado is None:
                return None
            else:
                return resultado[0] # Devolvemos el primer elemento de la fila (el id)
    
    @classmethod
    def obtener_materia(cls,id_materia):
        with Cursor() as cursor:
            valores = (id_materia,)
            logging.debug(f'{cls._SELECCIONAR_MATERIA_POR_ID} - Valores: {valores}')
            cursor.execute(cls._SELECCIONAR_MATERIA_POR_ID, valores)
            resultado = cursor.fetchone() # Recuperamos la primera fila de resultados
            if resultado is None:
                return None
            else:
                # Creamos un objeto Materia con los datos de la fila
                materia = Materia(resultado[0], resultado[1])
                # Establecemos el atributo id del objeto Materia
                materia.id_materia = resultado[0]
                logging.debug(f'Materia Obtenida: {materia}')
                return materia
    
if __name__ == '__main__':
    materias = MateriaDAO.leer_materias()
    for materia in materias:
        logging.debug(f'Id = {materia.id_materia} Nombre = {materia.nombre}')

    #materia = Materia(1, 'Matematicas avanzadas')
   # materia_agregada = MateriaDAO.crear_materia(materia)
    #logging.debug(f'Matera agregada: {materia_agregada}')

    #materia = Materia(5, 'Matematicas intermedia')
    #materia_actualizar = MateriaDAO.actualizar_materia(materia)
    #logging.debug(f'Materia actualizada: {materia_actualizar}')

    #materia = Materia(nombre='Matematicas intermedias')
    #materia_eliminada = MateriaDAO.eliminar_materia(materia)
    #ogging.debug(f'Alumno eliminado {materia_eliminada}')
            
