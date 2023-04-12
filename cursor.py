from conexion import logging  # Se importa el módulo logging
from conexion import Conexion  # Se importa la clase Conexion
from alumno import Alumno  # Se importa la clase Alumno

class Cursor:
    def __init__(self):
        self._cursor = None
        self._conexion = None
    
    def __enter__(self):
        logging.debug('Inicio del enter')  # Se muestra un mensaje de debug indicando que se ha iniciado el bloque with
        self._conexion = Conexion.conexion()  # Se obtiene una conexión a la base de datos
        self._cursor = self._conexion.cursor()  # Se obtiene un cursor a partir de la conexión
        return self._cursor
    
    def __exit__(self, tipo_exepcion, valor_exepcion, detalle_exepcion):
        logging.debug('Inicio del exit')  # Se muestra un mensaje de debug indicando que se ha iniciado el exit
        if valor_exepcion:
            self._conexion.rollback()  # Si ha ocurrido una excepción, se hace rollback de la transacción
            logging.error(f'Ocurrio un error: {valor_exepcion}, {tipo_exepcion}, {detalle_exepcion}')  # Se muestra un mensaje de error con los detalles de la excepción
        else:
            self._conexion.commit()  # Si no ha ocurrido una excepción, se hace commit de la transacción
            logging.debug('Se hizo commit')  # Se muestra un mensaje de debug indicando que se ha hecho commit
        self._cursor.close()  # Se cierra el cursor
        Conexion.liberar_conexion(self._conexion)  # Se libera la conexión a la base de datos



if __name__ == '__main__':
    alumno = Alumno(7,9,5,1)
    logging.debug(alumno)

    