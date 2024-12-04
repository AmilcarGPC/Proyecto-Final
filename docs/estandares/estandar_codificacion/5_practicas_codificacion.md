---
# docs/estandares/estandar_codificacion/5_practicas_codificacion.md
title: Prácticas de Codificación
description: Esta sección define las prácticas de codificación permitidas, limitadas y prohibidas en Python.
---

Este documento establece las prácticas fundamentales de codificación en Python, enfatizando claridad, mantenibilidad y rendimiento. Se definen patrones recomendados y antipatrones a evitar.


## 1. Estructuras de Control

### Instrucciones
- Preferir estructuras simples y lineales
- Evitar anidamiento excesivo
- Mantener bloques de código compactos
- Usar estructuras estándar de control de flujo (`if`, `for`, `while`, ...)
- Limitar operador ternario a una línea
- Preferir elif sobre else + if
- Los bloques if/for/while deben estar en múltiples líneas

### Mejores Prácticas
- Evitar else en loops
- Un break/continue por función
- Mantener flujo de control lineal

### Ejemplos
```python
# Correcto
valor = x if condicion else y

if valor < 0:
    return "negativo"
elif valor > 0:
    return "positivo"
else:
    return "cero"

if x > 5:
    print(x)
for i in range(3):
    print(i)
while x < 10:
    x += 1

# Incorrecto
valor = x if a > b else y if b > c else z  # ternario anidado

if valor < 0:
    return "negativo"
else:
    if valor > 0:  # debería usar elif
        return "positivo"
    else:
        return "cero"

if x > 5: print(x)
for i in range(3): print(i)
while x < 10: x += 1
```

### Verificación
- [ ] ¿Sin else en loops?
- [ ] ¿Un solo break/continue?
- [ ] ¿Ternarios simples?

## 2. Manejo de Errores

### Instrucciones
- Usar try/except específicos
- Limitar excepciones por bloque
- Documentar excepciones personalizadas
- Los bloques try/except deben estar en múltiples líneas

### Mejores Prácticas
- Mantener bloques try pequeños

### Ejemplos
```python
# Correcto
try:
    x = 1 / 0
except ZeroDivisionError:
    x = None

# Incorrecto
try: x = 1 / 0
except ZeroDivisionError: x = None
```

### Verificación
- [ ] ¿Excepciones específicas?
- [ ] ¿Bloques try concisos?
- [ ] ¿Manejo apropiado de errores?

## 3. Funciones y Métodos

### Instrucciones
- Mantener funciones simples y enfocadas
- Limitar parámetros y complejidad
- Evitar efectos secundarios
- Documentar comportamiento claramente
- No usar lambda functions
- Las definiciones de funciones deben estar en múltiples líneas
- Los bloques with deben estar en múltiples líneas

### Mejores Prácticas
- Un nivel de funciones anidadas
- Usar *args/**kwargs con moderación

### Ejemplos
```python
# Correcto
def es_par(x: int) -> bool:
    return x % 2 == 0

def funcion():
    return 42

with open("archivo.txt", "r") as archivo:
    datos = archivo.read()

# Incorrecto
es_par = lambda x: x % 2 == 0 

def funcion(): return 42

with open("archivo.txt", "r") as archivo: datos = archivo.read()
```

### Verificación
- [ ] ¿Sin lambdas?
- [ ] ¿Anidamiento simple?
- [ ] ¿Documentación clara?

## 4. Estructuras de Datos

### Instrucciones
- Usar tipos de datos estándar
- Limitar complejidad de estructuras
- Preferir inmutabilidad cuando sea posible
- Mantener estructuras planas
- List/Dict/Set comprehensions de una línea, no anidados
- Limitar uso de sets a operaciones básicas (add, remove, union, intersection)

### Mejores Prácticas
- Diccionarios con un nivel de anidamiento
- Evitar tuplas nombradas y tipos genéricos anidados

### Ejemplos
```python
# Correcto
numeros = [x for x in range(10) if x % 2 == 0]
configuracion = {"depurar": True, "config": {"puerto": 8000}}

# Incorrecto
matriz = [[x for x in range(5)] for y in range(5)]  # Anidado
profundo = {"a": {"b": {"c": 1}}}  # Demasiado anidamiento
```

### Verificación
- [ ] ¿Comprehensions simples?
- [ ] ¿Estructuras planas?
- [ ] ¿Uso moderado de collections?
- [ ] ¿Sin tipos complejos?

## 5. Asincronía y Concurrencia

### Instrucciones
- Limitar uso de asyncio
- Mantener código asíncrono simple
- Evitar mezclar sync/async
- Documentar comportamiento asíncrono

### Mejores Prácticas
- Un nivel de anidación async
- Evitar callbacks complejos
- Mantener tareas independientes

### Ejemplos
```python
# Correcto
async def obtener_datos(url: str) -> dict:
    async with aiohttp.ClientSession() as sesion:
        async with sesion.get(url) as respuesta:
            return await respuesta.json()

# Incorrecto
async def operacion_compleja():
    async def anidada():  # Anidamiento excesivo
        async def mas_profunda():  # Prohibido
            pass
```

### Verificación
- [ ] ¿Anidación simple?
- [ ] ¿Uso justificado?
- [ ] ¿Documentación clara?

## 6. Tipos y Type Hints

### Instrucciones
- Usar type hints básicos
- Evitar tipos genéricos complejos
- Mantener consistencia en anotaciones
- No usar TypeVar o tipos dinámicos

### Mejores Prácticas
- Solo List[T], Dict[K,V], Optional[T]
- Documentar tipos complejos
- Usar tipos estándar
- Evitar Any cuando sea posible

### Ejemplos
```python
# Correcto
def procesar_elementos(elementos: List[str]) -> Dict[str, int]:
    return {elemento: len(elemento) for elemento in elementos}

# Incorrecto
from typing import TypeVar, Generic  # Prohibido
T = TypeVar('T')  # Prohibido
```

### Verificación
- [ ] ¿Types hints simples?
- [ ] ¿Sin TypeVar?
- [ ] ¿Tipos estándar?
- [ ] ¿Documentación clara?

## 7. Clases y Herencia

### Instrucciones
- Usar herencia simple únicamente
- Prohibir herencia múltiple y mixins
- Limitar uso de propiedades
- Mantener interfaces simples
- Solo permitido el patrón Factory
- Prohibida la inyección de dependencias compleja (más de 2 niveles)

### Mejores Prácticas
- Clases abstractas solo para interfaces básicas
- Documentar herencia claramente
- Una responsabilidad principal y una de soporte máximo
- Usar constructor injection para dependencias simples
- Seguir este orden para métodos de clase:
    1. Docstring de clase
    2. Métodos dunder (__init__, __str__, etc)
    3. Métodos de clase (@classmethod)
    4. Métodos estáticos (@staticmethod)
    5. Propiedades (@property)
    6. Métodos públicos
    7. Métodos "protegidos" (_)
    8. Métodos "privados" (__)

### Ejemplos
```python
# Correct
class FabricaReporte:
    def __init__(self, config: dict):
        self.ruta_plantilla = config["ruta_plantilla"]
    
    def crear_reporte(self, tipo: str) -> Reporte:
        if tipo == "pdf":
            return ReportePDF(self.ruta_plantilla)
        elif tipo == "excel":
            return ReporteExcel(self.ruta_plantilla)
        raise ValueError("Tipo de reporte desconocido")

class Report(ABC): # Simple Interface
    @abstractmethod
    def generar(self) -> bytes: pass
    
    @abstractmethod
    def guardar(self, path: str) -> None: pass

# Wrong
class Servicio:
    def __init__(self, repo, cache, logger, validador, formateador):
        pass  # Inyección compleja prohibida
```

### Verificación
- [ ] ¿Sin herencia múltiple?
- [ ] ¿Sin mixins?
- [ ] ¿Properties simples?
- [ ] ¿Interfaces básicas?

## 8. Formateado de Strings

### Instrucciones
- Usar f-strings como método preferido
- Permitir str.format() cuando sea necesario
- Prohibir % formatting
- Limitar template strings

### Mejores Prácticas
- F-strings para casos simples
- Mantener strings legibles
- Documentar strings complejos

### Ejemplos
```python
# Correcto
nombre = "Juan"
edad = 30
mensaje = f"Nombre: {nombre}, Edad: {edad}"

plantilla = "Nombre: ${nombre}\nEdad: ${edad}"
resultado = plantilla.substitute(nombre=nombre, edad=edad)

# Incorrecto
mensaje = "Nombre: %s, Edad: %d" % (nombre, edad)  # formato % prohibido
plantilla_compleja = "${exterior${interior${profundo}}}"  # Demasiados niveles
```

### Verificación
- [ ] ¿Sin % formatting?
- [ ] ¿Uso preferente de f-strings?
