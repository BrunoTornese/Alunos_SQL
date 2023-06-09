from cursor import Cursor  # Importamos la clase Cursor de nuestro módulo de cursor
from conexion import logging  # Importamos el objeto logging de nuestro módulo de conexión
from alumno import Alumno  # Importamos la clase Alumno
from materia import Materia  # Importamos la clase Materia
from materias_manejos import MateriaDAO  # Importamos la clase MateriaDAO
from alumnos_manejos import AlumnoDAO  # Importamos la clase AlumnoDAO


class Alumno_MateriaDAO:
    def __init__(self, id_alumno=None, id_materia=None):
        self._id_alumno = id_alumno  # Se inicializa el atributo id_alumno con el valor recibido como parámetro
        self._id_materia = id_materia  # Se inicializa el atributo id_materia con el valor recibido como parámetro

    def __str__(self):
        # Se obtienen los objetos alumno y materia correspondientes a los IDs almacenados en el objeto AlumnoMateria
        alumno = AlumnoDAO.buscar_por_id(self._id_alumno)
        materia = MateriaDAO.buscar_por_id(self._id_materia)
        # Se devuelve una cadena de texto que representa al objeto AlumnoMateria en forma de "Alumno: nombre_apellido, Materia: nombre_materia"
        return f'Alumno: {alumno.nombre} {alumno.apellido}, Materia: {materia.nombre}'

    @property
    def id_alumno(self):
        return self._id_alumno  # Método getter para la propiedad id_alumno

    @id_alumno.setter
    def id_alumno(self, id_alumno):
        self._id_alumno = id_alumno  # Método setter para la propiedad id_alumno, que asigna el valor recibido como parámetro al atributo _id_alumno

    @property
    def id_materia(self):
        return self._id_materia  # Método getter para la propiedad id_materia

    @id_materia.setter
    def id_materia(self, id_materia):
        self._id_materia = id_materia  # Método setter para la propiedad id_materia, que asigna el valor recibido como parámetro al atributo _id_materia

    _VER_ASOCIACIONES = '''SELECT alumno.id, alumno.nombre, materia.id_materia, materia.nombre_materia 
    FROM alumno 
    INNER JOIN alumnos_materias ON alumno.id = alumnos_materias.alumno_id 
    INNER JOIN materia ON materia.id_materia = alumnos_materias.id_materia
    ''' # sentencia para ver los alumnos y sus materias
    _AGREGAR = "INSERT INTO alumnos_materias (alumno_id, id_materia) VALUES (%s, %s)" # Consulta SQL para agregar una asociación entre un alumno y una materia
    _SELECCIONAR_POR_ALUMNO = "SELECT * FROM alumnos_materias WHERE alumno_id = %s" # Consulta SQL para seleccionar todas las asociaciones de un alumno
    _SELECCIONAR_POR_NOMBRE = "SELECT id_materia, nombre FROM materia WHERE nombre = %s"# Consulta SQL para seleccionar todas las asociaciones de una materia
    _SELECCIONAR_POR_MATERIA = """ 
    SELECT alumno.id, alumno.nombre, alumno.apellido
    FROM alumno
    INNER JOIN alumnos_materias ON alumno.id = alumnos_materias.alumno_id
    INNER JOIN materia ON alumnos_materias.id_materia = materia.id_materia
    WHERE materia.nombre_materia = %s
""" # Selecciona los campos alumnos_materias.id, alumno.nombre, alumno.apellido y alumnos_materias.id_materia de la tabla alumnos_materias y los filtra por la columna nombre_materia de la tabla materia. Luego, une la tabla alumno mediante la columna id de la tabla alumnos_materias
    _ELIMINAR_ASOCIACION = "DELETE FROM alumnos_materias WHERE alumno_id = %s AND id_materia = %s;"

    @classmethod
    def ver_asociaciones(cls):
        with Cursor() as cursor:# Establecer conexión a la base de datos y crear objeto Cursor
            cursor.execute(cls._VER_ASOCIACIONES) # Sentencia a ejecutar
            alumnos = {} # Lista vacia de alumnos
            for registro in cursor.fetchall(): # Para cada registro 
                id, nombre_alumno, id_materia, nombre_materia = registro # Toma todos sus atributos
                if id not in alumnos:
                    alumnos[id] = {'nombre_alumno': nombre_alumno, 'materias': []} 
                alumnos[id]['materias'].append({'id_materia': id_materia, 'nombre_materia': nombre_materia})
            print(alumnos)  # imprimir el diccionario de alumnos con sus respectivas materias
            return alumnos

    @classmethod
    def agregar(cls, id_alumno, id_materia): #Funcion palra agregar asociacion a la base de datos
        with Cursor() as cursor:# Establecer conexión a la base de datos y crear objeto Cursor
            try:
                valores = (id_alumno, id_materia)# valores para ejecutar la funcion
                cursor.execute(cls._AGREGAR, valores)# Sentencia a ejecutar
                return cursor.rowcount
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                return 0
    
    @classmethod
    def seleccionar_por_alumno(cls, alumno):
        with Cursor() as cursor:
            valores = (alumno._id,)  # Se define una tupla con el ID del alumno
            logging.debug(f"Ejecutando consulta SQL para seleccionar registros por alumno {alumno.nombre} {alumno.apellido}")
            cursor.execute(cls._SELECCIONAR_POR_ALUMNO, valores)  # Se ejecuta la consulta SQL correspondiente al método y se pasan los valores de la tupla como parámetros
            registros = cursor.fetchall()  # Se obtienen todos los registros resultantes de la consulta
            alumnos_materias = []  # Se define una lista vacía para almacenar los objetos de tipo alumno_materia
            for registro in registros:  # Se recorren los registros obtenidos
                alumno_materia = {  # Se crea un diccionario con los datos de la asociación entre alumno y materia
                    "alumno": alumno,  # Se asigna el objeto alumno recibido como parámetro
                    "materia": None  # Se inicializa el atributo materia del diccionario en None
                }
                materias = MateriaDAO.leer_materias()  # Se obtienen todas las materias de la base de datos
                for materia in materias:  # Se recorren todas las materias
                    if materia.id_materia == registro[2]:  # Si se encuentra la materia correspondiente al ID almacenado en el registro
                        alumno_materia["materia"] = materia  # Se asigna la materia al atributo materia del diccionario
                        break  # Se sale del ciclo
                if alumno_materia["materia"] is not None:  # Si se encontró una materia correspondiente al registro
                    logging.debug(f"Se encontró registro de materia {alumno_materia['materia'].nombre} para el alumno {alumno.nombre} {alumno.apellido}")
                    alumnos_materias.append(alumno_materia)  # Se agrega el diccionario a la lista de alumnos_materias
                    logging.debug(F'Materias encontradas: {alumnos_materias}')
            return alumnos_materias  # Se devuelve la lista de alumnos_materias resultante
        
    @classmethod
    def seleccionar_por_materia(cls, materia):
        with Cursor() as cursor:
            valores = (materia.nombre,)  # Se define una tupla con el nombre de la materia
            logging.debug(f"Ejecutando consulta SQL para seleccionar registros por materia {materia.nombre}")
            cursor.execute(cls._SELECCIONAR_POR_MATERIA, valores)  # Se ejecuta la consulta SQL correspondiente al método y se pasan los valores de la tupla como parámetros
            registros = cursor.fetchall()  # Se obtienen todos los registros resultantes de la consulta
            alumnos_materias = []  # Se define una lista vacía para almacenar los objetos de tipo alumno_materia
            for registro in registros:
                alumno_materia = {
                    "alumno": None,
                    "materia": materia
                }
                alumnos = AlumnoDAO.seleccionar()
                for alumno in alumnos:
                    if alumno.id == registro[0]:
                        alumno_materia["alumno"] = alumno
                        break
                if alumno_materia["alumno"] is not None:
                    logging.debug(f"Se encontro registro de un alumno {alumno_materia['alumno'].nombre} para la materia {materia.nombre}")
                    alumnos_materias.append(alumno_materia)
            logging.debug(f"Alumnos encontrados: {alumnos_materias}")
            return alumnos_materias

 
    @classmethod
    def eliminar_asociacion(cls, alumno_nombre, alumno_apellido, materia_nombre):
        alumno_id = AlumnoDAO.obtener_id_alumno(alumno_nombre, alumno_apellido) # Obtiene el ID del alumno
        materia_id = MateriaDAO.obtener_id_materia(materia_nombre)# Obtiene el ID de la materia
        with Cursor() as cursor:
            logging.debug(f'Eliminando la asociación entre el alumno {alumno_nombre} {alumno_apellido} y la materia {materia_nombre}') # Ejecutar la consulta de eliminación de la asociación
            valores = (alumno_id, materia_id)
            cursor.execute(cls._ELIMINAR_ASOCIACION, valores)
            return cursor.rowcount # Devolver el número de filas afectadas
 

if __name__ == '__main__':
    asociaciones = Alumno_MateriaDAO.ver_asociaciones()
    print('Asociaciones de alumnos y materias:')
    for alumno_id, data in asociaciones.items():
        print(f"Alumno {data['nombre_alumno']} ({alumno_id}):")
        for materia in data['materias']:
            print(f"- {materia['nombre_materia']} ({materia['id_materia']})")

    #alumno1 = Alumno(id=52, nombre='Bruno', apellido='Tornese')
    #materia1 = Materia(10,'Fisica')
    #Alumno_MateriaDAO.agregar(alumno1.id, materia1.id_materia)

    #alumno_existente = Alumno(id=19, nombre='Alfredo', apellido='Sanchez')
    #materias = Alumno_MateriaDAO.seleccionar_por_alumno(alumno_existente)
    #logging.debug(materias)

    #materia = Materia(nombre='Geografia')
    #Alumno_MateriaDAO.seleccionar_por_materia(materia)

    #Alumno_MateriaDAO.eliminar_asociacion('Bruno','Tornese', 'Fisica')




    
  
