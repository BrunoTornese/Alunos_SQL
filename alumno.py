class Alumno:
    def __init__(self, id=None, nombre=None, apellido=None):
        # Constructor que inicializa los atributos del  Alumno.
        self._id = id
        self._nombre = nombre
        self._apellido = apellido

    def __str__(self):
        # Método que retorna una representación en forma de string del  Alumno.
        return f' Nombre: {self._nombre} Apellido: {self._apellido} Alumno: {self._id}'

    @property
    def id(self):
        # Método que retorna el valor del atributo id del  Alumno.
        return self._id

    @id.setter
    def id(self, _id):
        # Método que permite asignar un valor al atributo id del  Alumno.
        self._id = _id

    @property
    def nombre(self):
        # Método que retorna el valor del atributo nombre del  Alumno.
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        # Método que permite asignar un valor al atributo nombre del  Alumno.
        self._nombre = nombre

    @property
    def apellido(self):
        # Método que retorna el valor del atributo apellido del  Alumno.
        return self._apellido

    @apellido.setter
    def apellido(self, apellido):
        # Método que permite asignar un valor al atributo apellido del  Alumno.
        self._apellido = apellido


        