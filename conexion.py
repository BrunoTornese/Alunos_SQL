import logging  # Importamos el módulo logging
from psycopg2 import pool  # Importamos la clase pool del módulo psycopg2
import sys  # Importamos el módulo sys

# Configuramos el logger con el nivel DEBUG, un formato personalizado y dos handlers: uno que escribe en un archivo y otro que muestra por consola
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
    datefmt='%I:%M:%S %p',
    handlers=[
        logging.FileHandler('INFO.log'),
        logging.StreamHandler()
    ]
)

class Conexion:
    _DATABASE = 'alumnos'  # Nombre de la base de datos
    _USERNAME = 'postgres'  # Nombre de usuario
    _PASSWORD = 'admin'  # Contraseña
    _DB_PORT = '5432'  # Puerto de la base de datos
    _HOST = '127.0.0.1'  # Dirección IP del servidor de la base de datos
    _MIN_CON = 0  # Número mínimo de conexiones en el pool
    _MAX_CON = 20  # Número máximo de conexiones en el pool
    _pool = None  # Atributo de clase que almacenará la instancia del pool

    @classmethod
    def pool(cls):  # Método de clase que crea y devuelve una instancia del pool
        if cls._pool is None:  # Si el pool no existe, lo creamos
            try:
                cls._pool = pool.SimpleConnectionPool(
                    cls._MIN_CON,
                    cls._MAX_CON,
                    host=cls._HOST,
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    port=cls._DB_PORT,
                    database=cls._DATABASE
                )
                logging.debug(f'Se creo el pool de manera exitosa: {cls._pool}')  # Escribimos en el log que el pool se ha creado correctamente
                return cls._pool  # Devolvemos la instancia del pool
            except Exception as e:
                logging.error(F'ocurrio un error al obtener el pool {e}')  # Si ocurre algún error, lo escribimos en el log y salimos del programa
                sys.exit()
        else:  # Si el pool ya existe, lo devolvemos
            return cls._pool

    @classmethod
    def conexion(cls):  # Método de clase que devuelve una conexión del pool
        logging.debug(f'Obteniendo conexión del pool...')  # Escribimos en el log que estamos obteniendo una conexión del pool
        conexion = cls.pool().getconn()  # Obtenemos una conexión del pool
        logging.debug(f'Conexión obtenida del pool: {conexion}')  # Escribimos en el log que hemos obtenido una conexión
        return conexion

    @classmethod
    def liberar_conexion(cls, conexion):  # Método de clase que libera una conexión y la devuelve al pool
        logging.debug(f'Liberando un pool')  # Escribimos en el log que estamos liberando una conexión
        cls.pool().putconn(conexion)  # Liberamos la conexión y la devolvemos al pool
        logging.debug(f'Pool liberado: {conexion}')  # Escribimos en el log que hemos liberado una conexión

    
    @classmethod
    def cerrar_conexion(cls):  # Método de clase que cierra la conexión a la base de datos
        logging.debug(f'Cerrando conexion')  # Mensaje de registro que indica que se está cerrando la conexión
        cls.pool().closeall()  # Se utiliza el método closeall() para cerrar todas las conexiones de la piscina
        logging.debug(f'Conexion cerrada {Conexion}')  # Mensaje de registro que indica que la conexión ha sido cerrada y muestra el objeto Conexion


if __name__ == '__main__':
    conexion_ = Conexion.conexion()
    Conexion.liberar_conexion(conexion_)

    