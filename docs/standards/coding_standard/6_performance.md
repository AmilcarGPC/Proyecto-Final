---
# docs/standards/coding_standard/performance.md
title: Performance
description: Esta sección define las reglas y mejores prácticas para optimizar el rendimiento de código Python. Incluye ejemplos y recomendaciones.
---

Este documento establece las pautas para optimización y rendimiento del código Python, enfocándose en el uso eficiente de recursos y mejores prácticas de rendimiento.

## 1. Estructuras de Datos Permitidas

### Instrucciones
- Usar solo estas estructuras:
  * list (para secuencias ordenadas)
  * dict (para mapeos clave-valor)
  * set (para búsquedas rápidas)
- Tamaño máximo: 1000 elementos por colección

### Mejores Prácticas
- Preferir operaciones vectorizadas (numpy)
- Usar `set` para búsquedas frecuentes
- Evitar copias innecesarias de datos
- Liberar recursos explícitamente

### Ejemplos
```python
# Correct
users = []  # List for sequential iteration
cache = {}  # Dict for key-based search
unique_ids = set()  # Set for fast lookups

# Wrong
matrix = [[0] * 1000 for _ in range(1000)]  # Limit exceeded
```

### Verificación
- [ ] ¿Estructura de datos apropiada?
- [ ] ¿Tamaño de colecciones controlado?

## 2. Algoritmos y Complejidad

### Instrucciones
- Solo permitidos algoritmos O(n^3) o menores
- Usar búsqueda diccionario/set en lugar de lista

### Mejores Prácticas
- Evitar loops anidados
- Máximo un loop por función

### Ejemplos
```python
# Correct - O(n)
def find_sum(numbers: list) -> int:
    return sum(numbers)

# Correct - O(1)
def find_user(users: dict, user_id: str) -> dict:
    return users.get(user_id)

# Wrong - O(n^4)
def find_duplicates(items: list) -> list:
    duplicates = []
    for i in items:
        for j in items:
            for k in items: 
                for l in items:  # Too many loops
                    if i == j == k == l:
                        duplicates.append(i)
    return duplicates
```

### Verificación
- [ ] ¿Complejidad algorítmica optimizada?
- [ ] ¿Uso de búsqueda eficiente?
- [ ] ¿Evita loops anidados?
- [ ] ¿Uso de estructuras de datos apropiadas?

## 3. Manejo de Recursos

### Instrucciones
- Usar 'with' para archivos y recursos
- Un solo archivo abierto a la vez
- Cerrar recursos explícitamente
- No mantener archivos abiertos entre funciones

### Mejores Prácticas
- Evitar fugas de recursos

### Ejemplos
```python
# Correct
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

# Wrong
def bad_read():
    f = open('file.txt')  # With is not used
    data = f.read()
    return data  # File never closed
```

### Verificación
- [ ] ¿Solo usa estructuras permitidas?
- [ ] ¿Colecciones <= 1000 elementos?
- [ ] ¿Sin loops anidados?
- [ ] ¿Usa 'with' para recursos?