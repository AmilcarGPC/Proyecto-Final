ARCHIVO_VACIO = ""

SOLO_BLANCO = " "

SOLO_COMENTARIOS = """
# Comentario 1
# Comentario 2

"""

SOLO_DOCSTRINGS = '''
"""
Docstring 1
Docstring 2
"""

'''

FUNCION_BASICA = """
def funcion_simple() -> bool:
    return True
"""

FUNCION_CON_PARAMETROS = """
def funcion_con_parametros(param1: int, param2: int) -> int:
    return param1 + param2
"""

FUNCION_CON_PARAMETROS_Y_DOCSTRING = '''
def funcion_con_parametros(param1: int, param2: int) -> int:
    """
    Suma dos parámetros

    Args:
        param1 (int): Primer número
        param2 (int): Segundo número

    Returns:
        int: Suma de los dos números
    """
    return param1 + param2
'''

CLASE_BASICA = """
class ClaseSimple:

    pass
"""

CLASE_CON_METODOS = """
class ClaseConMetodos:

    def __init__(self):
        pass
    
    def metodo_1(self):
        pass
    
    def _metodo_2(self):
        pass
"""

CLASE_CON_METODOS_Y_DOCSTRING = '''
class ClaseConMetodos:

    def __init__(self):
        """
        Constructor de la clase
        """
        pass
    
    def metodo_1(self):
        """
        Primer método
        """
        pass
    
    def _metodo_2(self):
        """
        Segundo método
        """
        pass
'''

IF_ELIF_ELSE = """
if condicion:
    pass
elif otra_condicion:
    pass
else:
    pass
"""

FOR = """
for x in range(10):
    pass
"""

WHILE = """
while condicion:
    pass
"""

MATCH = """
match valor:
    case 1:
        pass
    case 2:
        pass
"""

LIST_COMPREHENSION = """
numeros = [x for x in range(10)]
"""

DICT_COMPREHENSION = """
pares = {x: x*2 for x in range(5)}
"""

SET_COMPREHENSION = """
impares = {x for x in range(10) if x % 2 != 0}
"""

GENERATOR_EXPRESSION = """
valores = (x for x in range(10))
"""

TERNARY = """
resultado = x if condicion else y
"""

WITH = """
with open("archivo.txt") as f:
    pass
"""

TRY_EXCEPT_FINALLY = """
try:
    pass
except Exception as e:
    pass
finally:
    pass
"""

PROPERTY = """
@property
def atributo(self):
    pass
"""

DECORATOR = """
@decorador
def funcion_decorada():
    pass
"""

INLINE_COMMENT = """
x = 1  # Comentario
"""

IMPORTACION_SIMPLE = """
import modulo
"""

IMPORTACION_MULTIPLE = """
import modulo1, modulo2
"""

IMPORTACION_FROM = """
from modulo import funcion
"""

ASIGNACION_SIMPLE = """
x = 1
"""

ASIGNACION_MULTIPLE = """
x, y, z = 1, 2, 3
"""