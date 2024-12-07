CASOS_EVALUACION = {
    'caso_basico': {
        'codigo': '''
class Simple:
    def metodo(self):
        return True
        
def funcion():
    return 42
''',
        'clases': [
            {'nombre': 'Simple', 'metodos': 1, 'lineas': 3},
            {'nombre': 'otros', 'metodos': 0, 'lineas': 2}
        ],
        'total_lineas': 5
    },

    'caso_herencia': {
        'codigo': '''
class Base:
    def metodo_base(self):
        pass

class Derivada(Base):
    def metodo_derivado(self):
        super().metodo_base()
        return True
''',
        'clases': [
            {'nombre': 'Base', 'metodos': 1, 'lineas': 3},
            {'nombre': 'Derivada', 'metodos': 1, 'lineas': 4},
            {'nombre': 'otros', 'metodos': 0, 'lineas': 0}
        ],
        'total_lineas': 7
    },

    'caso_mixto': {
        'codigo': '''
def funcion_global():
    return 42

class Primera:
    def __init__(self):
        self.x = 1

class Segunda:
    @property
    def prop(self):
        return True

variable = "test"
''',
        'clases': [
            {'nombre': 'Primera', 'metodos': 1, 'lineas': 3},
            {'nombre': 'Segunda', 'metodos': 1, 'lineas': 4},
            {'nombre': 'otros', 'metodos': 0, 'lineas': 3}
        ],
        'total_lineas': 10
    },

    'caso_anidado': {
        'codigo': '''
class Externa:
    class Interna:
        def metodo_interno(self):
            pass
            
    def metodo_externo(self):
        return True
''',
        'clases': [
            {'nombre': 'Externa', 'metodos': 1, 'lineas': 7},
            {'nombre': 'Externa.Interna', 'metodos': 1, 'lineas': 3},
            {'nombre': 'otros', 'metodos': 0, 'lineas': 0}
        ],
        'total_lineas': 7
    },

    'caso_decoradores': {
        'codigo': '''
class Servicios:
    @property
    def estado(self):
        return self._estado
        
    @estado.setter
    def estado(self, valor):
        self._estado = valor
''',
        'clases': [
            {'nombre': 'Servicios', 'metodos': 2, 'lineas': 7},
            {'nombre': 'otros', 'metodos': 0, 'lineas': 0}
        ],
        'total_lineas': 7
    }
}