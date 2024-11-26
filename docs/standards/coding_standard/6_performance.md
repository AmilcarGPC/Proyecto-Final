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

### Mejores Prácticas
- Preferir operaciones vectorizadas (numpy)
- Usar `set` para búsquedas frecuentes
- Evitar copias innecesarias de datos
- Liberar recursos explícitamente

### Ejemplos
```python
# Correcto
users = []  # Lista para iteración secuencial
cache = {}  # Diccionario para búsqueda por clave
unique_ids = set()  # Set para búsquedas rápidas
```

### Verificación
- [ ] ¿Estructura de datos apropiada?
- [ ] ¿Tamaño de colecciones controlado?
as?