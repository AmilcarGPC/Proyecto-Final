CASOS_EVALUACION = {
    'caso_poo': {
        'codigo': '''
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

class Volador:
    def volar(self):
        return "Estoy volando"

@property
def altura_vuelo(self):
    return self._altura

class Pajaro(Animal, Volador):
    def __init__(self, nombre, altura):
        super().__init__(nombre)
        self._altura = altura
''',
        'lineas_logicas': 8,
        'lineas_fisicas': 13
    },

    'caso_funcional': {
        'codigo': '''
def procesar_datos(numeros):
    resultados = [x**2 for x in numeros if x > 0]
    
    def filtrar_pares(lista):
        return [x for x in lista if x % 2 == 0]
    
    return filtrar_pares(resultados)

datos = range(-5, 6)
resultado = procesar_datos(datos)
''',
        'lineas_logicas': 4,
        'lineas_fisicas': 7
    },

    'caso_archivos': {
        'codigo': '''
try:
    with open('datos.txt', 'r') as archivo:
        lineas = [linea.strip().upper() for linea in archivo]
except FileNotFoundError:
    print("Archivo no encontrado")
finally:
    resultado = {
        'total_lineas': len(lineas) if 'lineas' in locals() else 0,
        'estado': 'completado'
    }
''',
        'lineas_logicas': 4,
        'lineas_fisicas': 7
    },

    'caso_avanzado': {
        'codigo': '''
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

gen = fibonacci_generator()
primeros_cinco = [next(gen) for _ in range(5)]
factoriales = map(factorial, primeros_cinco)
''',
        'lineas_logicas': 5,
        'lineas_fisicas': 14
    }
}