from conexion import logging  # importamos el módulo de logging
from alumno import Alumno  # importamos la clase Alumno
from cursor import Cursor  # importamos la clase Cursor

class AlumnoDAO:
    _SELECCIONAR = 'SELECT id, nombre, apellido FROM alumno'  # query para seleccionar todos los registros de la tabla alumno
    _INSERTAR = 'INSERT INTO alumno(Nombre,Apellido) VALUES (%s, %s)'  # query para insertar un nuevo registro en la tabla alumno
    _ACTUALIZAR = 'UPDATE alumno SET  Nombre=%s, Apellido=%s WHERE id=%s '  # query para actualizar un registro de la tabla alumno
    _ELIMINAR= 'DELETE FROM alumno WHERE id=%s'  # query para eliminar un registro de la tabla alumno

    @classmethod
    def insertar(cls, alumno):
        with Cursor() as cursor:
            logging.debug(f'Agregando al alumno: {alumno}')  # agregamos un log con información del alumno a agregar
            valores = (alumno._nombre, alumno._apellido)  # obtenemos los valores del alumno a agregar
            logging.debug(f'Valores a agregar: {valores}')  # agregamos un log con los valores a agregar
            cursor.execute(cls._INSERTAR, valores)  # ejecutamos el query de inserción con los valores del alumno
            logging.debug(f'Alumno agregado: {alumno}')  # agregamos un log con información del alumno agregado
            return cursor.rowcount  # retornamos la cantidad de filas afectadas por la operación de inserción
    
    @classmethod
    def eliminar(cls,alumno):
        with Cursor() as cursor:
            logging.debug(F'Alumno eliminado con id: {alumno._id}')  # agregamos un log con información del alumno a eliminar
            valores = (alumno._id,)  # obtenemos el valor del id del alumno a eliminar
            cursor.execute(cls._ELIMINAR,valores)  # ejecutamos el query de eliminación con el id del alumno
            return cursor.rowcount  # retornamos la cantidad de filas afectadas por la operación de eliminación

    @classmethod
    def seleccionar(cls):
        with Cursor() as cursor:
            cursor.execute(cls._SELECCIONAR)  # ejecutamos el query de selección
            registros = cursor.fetchall()  # obtenemos todos los registros resultantes de la consulta
            alumnos = []  # inicializamos una lista para almacenar los objetos Alumno
            for registro in registros:
                alumno = Alumno(registro[0], registro[1], registro[2])  # creamos un objeto Alumno con los datos del registro
                alumnos.append(alumno)  # agregamos el objeto Alumno a la lista de alumnos
            return alumnos  # retornamos la lista de alumnos
        
    @classmethod
    def actualizar(cls, alumno):
        with Cursor() as cursor:
            valores = (alumno._nombre, alumno._apellido, alumno._id)  # obtenemos los valores del alumno a actualizar
            cursor.execute(cls._ACTUALIZAR, valores)  # ejecutamos el query de actualización con los valores del alumno
            logging.debug(f'Alumno actualizado: {alumno}')  # agregamos un log con información del alumno actualizado
            return cursor.rowcount  # retornamos la cantidad de filas afectadas por la operación de actualización


                                

if __name__ == '__main__':
    alumno1 = AlumnoDAO.seleccionar()
    for alumno in alumno1:
      logging.debug(alumno)

    #alumno = Alumno(2,'Alfredo', 'Sanchez')
    #alumno_agregado = AlumnoDAO.insertar(alumno)
    #logging.debug(f'Alumno agregado: {alumno_agregado}')

    #alumno = Alumno(16, 'Carlos', 'Perez')
    #alumno_actualizar = AlumnoDAO.actualizar(alumno)
    #logging.debug(f'Alumno actualizado: {alumno_actualizar}')

    #alumno = Alumno(17)
    #alumno_eliminado = AlumnoDAO.eliminar(alumno)
    #logging.debug(f'Alumno eliminado {alumno_eliminado}')





