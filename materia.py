class Materia:
    # Constructor de la clase, inicializa las propiedades de la materia.
    def __init__(self, id_materia= None, nombre = None):
        self._nombre = nombre # Nombre de la materia.
        self._id_materia = id_materia # Identificador de la materia.
        self.alumnos = []

    # Método que devuelve una representación en forma de cadena de la materia.
    def __str__(self):
        return f'Materia: {self._nombre} Id: {self._id_materia}'

    # Método getter para la propiedad del nombre de la materia.
    @property
    def nombre(self):
        return self._nombre

    # Método getter para la propiedad del identificador de la materia.
    @property
    def id_materia(self):
        return self._id_materia

    # Método setter para la propiedad del identificador de la materia.
    @id_materia.setter
    def id_materia(self, _id_materia):
        self._id_materia = _id_materia


    


