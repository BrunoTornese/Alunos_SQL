from cursor import Cursor  # Importamos la clase Cursor de nuestro módulo de cursor
from conexion import logging  # Importamos el objeto logging de nuestro módulo de conexión
from alumno import Alumno  # Importamos la clase Alumno
from materia import Materia  # Importamos la clase Materia
from materias_manejos import MateriaDAO  # Importamos la clase MateriaDAO
from alumnos_manejos import AlumnoDAO  # Importamos la clase AlumnoDAO


class AlumnoMateriaDAO:
    _AGREGAR = "INSERT INTO alumno_materia (alumno_id, materia_id) VALUES (%s, %s)"  # Consulta SQL para agregar una asociación entre un alumno y una materia
    _SELECCIONAR_POR_ALUMNO = "SELECT * FROM alumno_materia WHERE alumno_id = %s"  # Consulta SQL para seleccionar todas las asociaciones de un alumno
    _SELECCIONAR_POR_MATERIA = "SELECT * FROM alumno_materia WHERE materia_id = %s"  # Consulta SQL para seleccionar todas las asociaciones de una materia
    _ELIMINAR_POR_ALUMNO = "DELETE FROM alumno_materia WHERE alumno_id = %s"  # Consulta SQL para eliminar todas las asociaciones de un alumno
    _ELIMINAR_POR_MATERIA = "DELETE FROM alumno_materia WHERE materia_id = %s"  # Consulta SQL para eliminar todas las asociaciones de una materia
    _ELIMINAR_ASOCIACION = "DELETE FROM alumnos_materias WHERE alumno_id = %s AND materia_id = %s"  # Consulta SQL para eliminar una asociación específica entre un alumno y una materia

    
    @classmethod
    def agregar(cls, alumno, materia):
        with Cursor() as cursor:  # Usamos un contexto with para asegurarnos de que el cursor se cierre después de usarlo
            valores = (alumno.id_alumno, materia.id_materia)  # Creamos una tupla con los valores para la consulta SQL
            cursor.execute(cls._AGREGAR, valores)  # Ejecutamos la consulta SQL con los valores
            logging.debug(f"Alumno {alumno.nombre} asociado a materia {materia.nombre}")  # Escribimos un mensaje de registro en el archivo de log
            return cursor.rowcount  # Devolvemos el número de filas afectadas por la consulta SQL
    
    @classmethod
    def seleccionar_por_alumno(cls, alumno):
        with Cursor() as cursor:
            valores = (alumno.id_alumno,)  # Se define una tupla con el ID del alumno
            cursor.execute(cls._SELECCIONAR_POR_ALUMNO, valores)  # Se ejecuta la consulta SQL correspondiente al método y se pasan los valores de la tupla como parámetros
            registros = cursor.fetchall()  # Se obtienen todos los registros resultantes de la consulta
            alumnos_materias = []  # Se define una lista vacía para almacenar los objetos de tipo alumno_materia
            for registro in registros:  # Se recorren los registros obtenidos
                alumno_materia = {  # Se crea un diccionario con los datos de la asociación entre alumno y materia
                    "alumno": alumno,  # Se asigna el objeto alumno recibido como parámetro
                    "materia": MateriaDAO.seleccionar_por_id(registro[2])  # Se busca la materia correspondiente al ID almacenado en el registro y se asigna al diccionario
                }
                alumnos_materias.append(alumno_materia)  # Se agrega el diccionario a la lista de alumnos_materias
            return alumnos_materias  # Se devuelve la lista de alumnos_materias resultante
    
    @classmethod
    def seleccionar_por_materia(cls, materia):
        with Cursor() as cursor:
            valores = (materia.id_materia,)  # Se define una tupla con el ID de la materia
            cursor.execute(cls._SELECCIONAR_POR_MATERIA, valores)  # Se ejecuta la consulta SQL correspondiente al método y se pasan los valores de la tupla como parámetros
            registros = cursor.fetchall()  # Se obtienen todos los registros resultantes de la consulta
            alumnos_materias = []  # Se define una lista vacía para almacenar los objetos de tipo alumno_materia
            for registro in registros:  # Se recorren los registros obtenidos
                alumno_materia = {  # Se crea un diccionario con los datos de la asociación entre alumno y materia
                    "alumno": AlumnoDAO.seleccionar_por_id(registro[1]),  # Se busca el alumno correspondiente al ID almacenado en el registro y se asigna al diccionario
                    "materia": materia  # Se asigna el objeto materia recibido como parámetro
                }
                alumnos_materias.append(alumno_materia)  # Se agrega el diccionario a la lista de alumnos_materias
            return alumnos_materias  # Se devuelve la lista de alumnos_materias resultante
    
    @classmethod
    def eliminar_por_alumno(cls, alumno):
        with Cursor() as cursor:
            valores = (alumno.id_alumno,)  # Se define una tupla con el ID del alumno
            cursor.execute(cls._ELIMINAR_POR_ALUMNO, valores)  # Se ejecuta la consulta SQL correspondiente al método y se pasan los valores de la tupla como parámetros
            logging.debug(f"Todas las asociaciones del alumno {alumno.nombre} eliminadas")  # Se escribe un mensaje en el log informando de la eliminación de las asociaciones
            return cursor.rowcount  # Se devuelve el número de registros afectados por la eliminación
    
    
    @classmethod
    def eliminar_por_materia(cls, materia):
        # Inicia una transacción con el cursor
        with Cursor() as cursor:
            # Crea una tupla con el ID de la materia a eliminar
            valores = (materia.id_materia,)
            # Ejecuta la sentencia SQL para eliminar las asociaciones con la materia
            cursor.execute(cls._ELIMINAR_POR_MATERIA, valores)
            # Registra un mensaje de debug indicando que se eliminaron las asociaciones con la materia
            logging.debug(f"Todas las asociaciones de la materia {materia.nombre} eliminadas")
            # Retorna el número de filas eliminadas por la sentencia SQL
            return cursor.rowcount

    @classmethod
    def eliminar_asociacion(cls, alumno_id, materia_id):
        # Inicia una transacción con el cursor
        with Cursor() as cursor:
            # Registra un mensaje de debug indicando que se eliminará la asociación entre un alumno y una materia
            logging.debug(f'Eliminando la asociación entre el alumno {alumno_id} y la materia {materia_id}')
            # Crea una tupla con los IDs del alumno y la materia para eliminar la asociación
            valores = (alumno_id, materia_id)
            # Ejecuta la sentencia SQL para eliminar la asociación entre el alumno y la materia
            cursor.execute(cls._ELIMINAR_ASOCIACION, valores)
            # Retorna el número de filas eliminadas por la sentencia SQL
            return cursor.rowcount

