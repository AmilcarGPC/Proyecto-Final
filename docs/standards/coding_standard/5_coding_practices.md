---
# docs/standards/coding_standard/coding_practices.md
title: Prácticas de Codificación
description: Esta sección define las prácticas de codificación permitidas, limitadas y prohibidas en Python.
---

Este documento establece las prácticas fundamentales de codificación en Python, enfatizando claridad, mantenibilidad y rendimiento. Se definen patrones recomendados y antipatrones a evitar.


## 1. Estructuras de Control

### Instrucciones
- Preferir estructuras simples y lineales
- Evitar anidamiento excesivo
- Mantener bloques de código compactos
- Usar estructuras estándar de control de flujo
- Limitar operador ternario a una línea
- Match/case: máximo 5 casos

### Mejores Prácticas
- Máximo 3 niveles de anidamiento
- Evitar else en loops
- Un break/continue por función
- Preferir elif sobre else + if
- Mantener flujo de control lineal

### Ejemplos
```python
# Correct
for item in items:
    if not item.is_valid():
        continue
    process_item(item)

value = x if condition else y

match status:
    case "active":
        process_active()
    case "inactive":
        process_inactive()
    case _:
        process_default()

if value < 0:
    return "negative"
elif value > 0:
    return "positive"
else:
    return "zero"

# Wrong
for item in items:
    if item.is_valid():
        process_item(item)
    else:
        continue  # unnecessary else

value = x if a > b else y if b > c else z  # nested ternary

match status:  # Too many cases
    case "a": pass
    case "b": pass
    case "c": pass
    case "d": pass
    case "e": pass
    case "f": pass

if value < 0:
    return "negative"
else:
    if value > 0:  # Should use elif instead
        return "positive"
    else:
        return "zero"
```

### Verificación
- [ ] ¿Anidamiento <= 3 niveles?
- [ ] ¿Sin else en loops?
- [ ] ¿Un solo break/continue?
- [ ] ¿Ternarios simples?

## 2. Manejo de Errores

### Instrucciones
- Usar try/except específicos
- Limitar excepciones por bloque
- Documentar excepciones personalizadas
- Evitar suppressión general de errores

### Mejores Prácticas
- Máximo 3 excepciones por bloque
- No usar except sin tipo
- Mantener bloques try pequeños
- Usar context managers para recursos

### Ejemplos
```python
# Correct
try:
    value = process_data(raw_data)
except ValueError as e:
    logger.error(f"Invalid data: {e}")
except KeyError as e:
    logger.error(f"Missing key: {e}")
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    raise

# Wrong
try:
    # A lot of code here...
except:  # Captures everything without discriminating
    pass
```

### Verificación
- [ ] ¿≤ 3 excepciones por bloque?
- [ ] ¿Excepciones específicas?
- [ ] ¿Bloques try concisos?
- [ ] ¿Manejo apropiado de errores?

## 3. Funciones y Métodos

### Instrucciones
- Mantener funciones simples y enfocadas
- Limitar parámetros y complejidad
- Limitar los With statements a máximo 2 niveles
- Evitar efectos secundarios
- Documentar comportamiento claramente
- No usar lambda functions
- Evitar closures
- Limitar *args/**kwargs a casos específicos
- Limitar map/filter a casos simples
- No usar reduce()

### Mejores Prácticas
- Máximo 2 decoradores por función
- Un nivel de funciones anidadas
- Usar *args/**kwargs con moderación

### Ejemplos
```python
# Correct
@validate_input
@log_execution
def process_data(data: list) -> dict:
    result = {}
    for item in data:
        result[item.id] = item.value
    return result

def insert_data(*args, **kwargs):  # Justified use for wrappers
    pass

with open('file1.txt') as f1, open('file2.txt') as f2:
    process_files(f1, f2)

# Wrong
def process(data):
    def nested1():
        def nested2():  # Too much nesting
            pass
    return lambda x: x * 2  # Lambda prohibited

def outer():
    x = 1
    def closure():  # Closure prohibited
        return x
    return closure

with open('f1.txt') as f1:
    with open('f2.txt') as f2:
        with open('f3.txt') as f3:  # Too many levels
            pass

from functools import reduce  # reduce() prohibited
```

### Verificación
- [ ] ¿≤ 2 decoradores?
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
- Usar collections.Counter y defaultdict con moderación, 1 por módulo como máximo
- Evitar tuplas nombradas y tipos genéricos anidados

### Ejemplos
```python
# Correct
numbers = [x for x in range(10) if x % 2 == 0]
settings = {"debug": True, "config": {"port": 8000}}

# Wrong
matrix = [[x for x in range(5)] for y in range(5)]  # Nested
deep = {"a": {"b": {"c": 1}}}  # Too much nesting
```

### Verificación
- [ ] ¿Comprehensions simples?
- [ ] ¿Estructuras planas?
- [ ] ¿Uso moderado de collections?
- [ ] ¿Sin tipos complejos?

## 5. Logging y Debugging

### Instrucciones
- Usar logging library en lugar de print
- Establecer niveles de log apropiados
- Mantener mensajes informativos
- Evitar logging excesivo

### Mejores Prácticas
- Un logger por módulo
- Mensajes claros y estructurados
- No usar print para debugging
- Remover código de debug en producción

### Ejemplos
```python
# Correct
import logging

logger = logging.getLogger(__name__)

def process_order(order_id: str) -> None:
    logger.info(f"Processing order {order_id}")
    try:
        order = get_order(order_id)
        logger.debug(f"Order details: {order}")
    except OrderNotFound as e:
        logger.error(f"Order {order_id} not found: {e}")

# Wrong
def process_order(order_id):
    print(f"Processing {order_id}")  # Use print for logging
    print(locals())  # Debug with print
```

### Verificación
- [ ] ¿Usa logging library?
- [ ] ¿Niveles apropiados?
- [ ] ¿Sin prints?
- [ ] ¿Mensajes claros?

## 6. Asincronía y Concurrencia

### Instrucciones
- Limitar uso de asyncio
- Mantener código asíncrono simple
- Evitar mezclar sync/async
- Documentar comportamiento asíncrono

### Mejores Prácticas
- Un nivel de anidación async
- Usar context managers async
- Evitar callbacks complejos
- Mantener tareas independientes

### Ejemplos
```python
# Correct
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Wrong
async def complex_operation():
    async def nested():  # Excessive nesting
        async def deeper():  # Prohibited
            pass
```

### Verificación
- [ ] ¿Anidación simple?
- [ ] ¿Uso justificado?
- [ ] ¿Documentación clara?
- [ ] ¿Context managers apropiados?

## 7. Metaprogramación y Reflection

### Instrucciones
- Evitar metaprogramación compleja
- No usar eval() o exec()
- Limitar uso de getattr/setattr
- Prohibir monkey patching

### Mejores Prácticas
- Máximo 3 usos de getattr/setattr por clase
- No usar globals()/locals()
- Evitar metaclases y descriptores
- No modificar clases en runtime

### Ejemplos
```python
# Correct
def get_attribute(obj: object, attr_name: str) -> Any:
    if hasattr(obj, attr_name):
        return getattr(obj, attr_name)
    return None

# Wrong
result = eval(user_input)  # Prohibited
globals()['dynamic_var'] = 42  # Prohibited
```

### Verificación
- [ ] ¿Sin eval/exec?
- [ ] ¿Sin modificación runtime?
- [ ] ¿Uso limitado de getattr?
- [ ] ¿Sin metaclases?

## 8. Tipos y Type Hints

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
# Correct
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Wrong
from typing import TypeVar, Generic  # Prohibited
T = TypeVar('T')  # Prohibited
```

### Verificación
- [ ] ¿Types hints simples?
- [ ] ¿Sin TypeVar?
- [ ] ¿Tipos estándar?
- [ ] ¿Documentación clara?

## 9. Clases y Herencia

### Instrucciones
- Usar herencia simple únicamente
- Prohibir herencia múltiple y mixins
- Limitar uso de propiedades
- Mantener interfaces simples
- Máximo 2 responsabilidades por clase
- Interfaces limitadas a 3 métodos máximo
- Solo permitido el patrón Factory
- Prohibida la inyección de dependencias compleja (más de 2 niveles)

### Mejores Prácticas
- Properties solo para getters/setters simples
- Clases abstractas solo para interfaces básicas
- Evitar jerarquías profundas (máximo 2 niveles)
- Documentar herencia claramente
- Una responsabilidad principal y una de soporte máximo
- Usar constructor injection para dependencias simples

### Ejemplos
```python
# Correct
class ReportFactory: # Factory Pattern
    def __init__(self, config: dict):
        self.template_path = config["template_path"]
    
    def create_report(self, type: str) -> Report:
        if type == "pdf":
            return PDFReport(self.template_path)
        elif type == "excel":
            return ExcelReport(self.template_path)
        raise ValueError("Unknown report type")

class Report(ABC): # Simple Interface (maximum 3 methods)
    @abstractmethod
    def generate(self) -> bytes: pass
    
    @abstractmethod
    def save(self, path: str) -> None: pass

# Wrong
class Repository(ABC):
    def create(self): pass
    def read(self): pass
    def update(self): pass
    def delete(self): pass  # Too many methods in interface, exceeds the limit

# Complex injection prohibited
class Service:
    def __init__(self, repo, cache, logger, validator, formatter):
        pass  # Too many dependencies
```

### Verificación
- [ ] ¿Sin herencia múltiple?
- [ ] ¿Sin mixins?
- [ ] ¿Properties simples?
- [ ] ¿Interfaces básicas?

## 10. Formateado de Strings

### Instrucciones
- Usar f-strings como método preferido
- Permitir str.format() cuando sea necesario
- Prohibir % formatting
- Limitar template strings

### Mejores Prácticas
- F-strings para casos simples
- Template strings: máximo 2 niveles, 100 caracteres
- Mantener strings legibles
- Documentar strings complejos

### Ejemplos
```python
# Correct
name = "John"
age = 30
message = f"Name: {name}, Age: {age}"

# Template con límites
template = "Name: ${name}\nAge: ${age}"
result = template.substitute(name=name, age=age)

# Wrong
message = "Name: %s, Age: %d" % (name, age)  # % formatting prohibited
complex_template = "${outer${inner${deepest}}}"  # Too many levels
```

### Verificación
- [ ] ¿Sin % formatting?
- [ ] ¿Template strings <= 2 niveles?
- [ ] ¿Template strings <= 100 caracteres?
- [ ] ¿Uso preferente de f-strings?
