# Sistema de Conteo de Líneas Físicas y Lógicas en Python
[![Licencia MIT - Permite uso comercial y modificaciones](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version de Python - Compatible con Python 3.8 o superior](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

Una herramienta Python para contar líneas de código físicas y lógicas escritas en lenguaje python (.py) siguiendo estándares propios.

## Características
- 📊 Conteo de líneas físicas (PLOC)
- 🔍 Conteo de líneas lógicas (LLOC)
- ✂️ Formateo de código a 80 caracteres
- 💾 Persistencia de métricas
- 📈 Visualización de historial
- 🎨 Salida en consola con colores

## Tabla de Contenidos
- [Inicio Rápido](#inicio-rápido)
- [Requisitos](#requisitos)
  - [Requisitos del Sistema](#requisitos-del-sistema)
  - [Dependencias de Python](#dependencias-de-python)
- [Instalación](#instalación)
- [Uso](#uso)
  - [Comandos Básicos](#comandos-básicos)
  - [Formateo de Código](#formateo-de-código)
- [Ejemplos](#ejemplos)
  - [Análisis Básico](#1-análisis-básico-de-archivos)
  - [Seguimiento Histórico](#2-seguimiento-histórico)
  - [Análisis Complejo](#3-análisis-de-archivo-complejo)
  - [Formateo](#4-ejemplos-de-formateo)
- [Documentación](#documentación)
  - [Cálculo de Métricas](#cálculo-de-métricas)
  - [Formateo de Código](#opciones-de-formateo-de-código)
  - [Manejo de Errores](#manejo-de-errores)
  - [Cumplimiento de Estándares](#cumplimiento-de-estándares)
  - [Almacenamiento](#almacenamiento)
- [Licencia](#licencia)

## Inicio Rápido

```bash
# 1. Instala el paquete
pip install -e .

# 2. Ejecuta el análisis en un archivo
contador_lineas data/ejemplo.py

# 3. Visualiza los resultados en formato de tabla
contador_lineas data/ejemplo.py -t
```

## Requisitos

### Requisitos del Sistema
- Windows 10/11
- Python 3.8 o superior
- 50MB de espacio en disco

### Dependencias de Python

Las dependencias se instalan automáticamente al instalar el paquete, pero se incluyen aquí para referencia:
- colorama
- tabulate

## Instalación

### Pre-requisitos
- Python 3.x
- pip package manager

```bash
# Instalar el paquete
pip install -e .

# Verificar la instalación
contador_lineas --version
```

## Uso

### Comandos Básicos

Comandos básicos para usar la herramienta:

```bash
# Analiza un unico archivo
contador_lineas ruta/archivo.py

# Muetsra las métricas del archivo
contador_lineas ruta/archivo.py -t

# View metrics history
contador_lineas -tc
```

### Formateo de Código

La herramienta incluye capacidades de formateo de código automático:

```bash
# Formatea el archivo a 80 caracteres por línea
contador_lineas ruta/archivo.py --format

# Formatea y muestra métricas
contador_lineas ruta/archivo.py --format -t
```


## Ejemplos

### 1. Análisis Básico de Archivos
```python
# ejemplo.py
def hola() -> bool:
    print("Hola Mundo")
    return True

# Ejecutar análisis
contador_lineas ejemplo.py
```
Salida:
```
LOC físicas: 3
LOC lógicas: 1
```

### 2. Seguimiento Histórico
```bash
# Analizar múltiples archivos
contador_lineas archivo1.py
contador_lineas archivo2.py

# Ver historial en formato tabla
contador_lineas -tc
```

### 3. Análisis de Archivo Complejo
```python
# complejo.py
class Calculadora:
    """
    Una clase calculadora simple
    """
    def sumar(self, a: int, b: int) -> int:
        return a + b

    def restar(self, a: int, b: int) -> int:
        return a - b

# Análisis con métricas detalladas
contador_lineas complejo.py -t
```

### 4. Ejemplos de Formateo
```python
# funcion_larga.py
def funcion_larga_con_muchos_argumentos(argumento1: int, argumento2: int, argumento3: int) -> int:
    return argumento1 + argumento2 + argumento3

# Ejecutar análisis
contador_lineas funcion_larga.py --format
```
Salida:
```python
def funcion_larga_con_muchos_argumentos(
        argumento1: int,
        argumento2: int,
        argumento3: int) -> int:
    return argumento1 + argumento2 + argumento3
```

## Documentación

### Cálculo de Métricas

> Todas las métricas siguen nuestro estándar de conteo personalizado definido en [`docs/standards/counting_standard.md`](docs/standards/counting_standard.md)

#### Líneas Físicas (PLOC)
Basado en la versión 1.2 de nuestro estándar de conteo, incluye:

**Incluido:**
- Declaraciones de importación (1 LOC por import, N para múltiples imports)
- Asignaciones simples (`x = 1` → 1 LOC)
- Asignaciones múltiples (`x, y = 1, 2` → 2 LOC)
- Código con comentarios en línea (solo cuenta el código)
- Declaraciones pass
- Cada línea en estructuras de control

**Reglas Multi-línea:**
1. Continuaciones explícitas:
```python
result = value1 + \   # 1 LOC total
         value2
```

2. Agrupación implícita:
```python
data = (             # 1 LOC total
    value1,
    value2,
    value3
)
```

3. Declaraciones de listas/diccionarios:
```python
items = [           # 1 LOC total
    item1,
    item2,
    item3
]
```

**No Contado como PLOC:**
- Líneas vacías
- Líneas shebang (`#!/usr/bin/env python`)
- Docstrings de módulos
- Comentarios/documentación

#### Líneas Lógicas (LLOC)
Siguiendo las especificaciones de nuestro estándar de conteo:

**Incluido:**
- Definiciones de funciones/métodos
- Definiciones de clases
- Estructuras de control (if, for, while)
- Expresiones match
- Comprehensions de listas/diccionarios/conjuntos
- Generators
- Operadores ternarias
- Bloques with
- Bloques try
- Propiedades y decoradores

Para reglas detalladas y especificaciones, consulte:
- [Documentación del Estándar de Conteo](docs/standards/counting_standard.md)
- [Documentación en Línea](https://docs-proyecto-final.vercel.app/)

### Opciones de Formateo de Código
- Longitud máxima de línea: 80 caracteres
- Mantiene la funcionalidad del código
- Maneja:
  - Declaraciones largas de funciones
  - Cadenas multi-línea
  - Expresiones complejas
  - Bloques de comentarios
  - Declaraciones de importación

### Manejo de Errores

Errores comunes y soluciones:

#### Violaciones del Estándar
| Mensaje de Error | Solución | Ejemplo |
|--------------|----------|----------|
| `El archivo debe tener al menos una línea de código` | Agregar código significativo al archivo | Crear funciones, clases o declaraciones |
| `La estructura [nodo.tipo] debe tener contenido` | Agregar contenido a estructuras vacías | `if x == 0: return -1` → `if x == 0: \nreturn -1` |
| `No se permiten varias declaraciones en una línea` | Dividir declaraciones en líneas separadas | `x = 1; y = 2` → `x = 1\ny = 2` |
| `No se permiten operadores ternarios/comprehension/generator anidados` | Simplificar expresiones anidadas | Usar declaraciones separadas o bucles |
| `No se permiten expresiones lambda` | Usar definiciones regulares de funciones | `lambda x: x+1` → `def add_one(x): \nreturn x+1` |

#### Validación de Archivos
| Mensaje de Error | Solución |
|--------------|----------|
| `El archivo '{ruta}' no fue encontrado` | Verificar que la ruta del archivo existe |
| `La ruta '{ruta}' no es un archivo` | Comprobar que la ruta apunta a un archivo, no a un directorio |
| `El archivo '{ruta}' debe tener extensión .py` | Asegurar que el archivo tiene extensión .py |

#### Errores de Uso
| Mensaje de Error | Solución |
|--------------|----------|
| `Error: Se requiere el archivo cuando no se usa -tc` | Proporcionar ruta del archivo o usar bandera -tc |

### Cumplimiento de Estándares

Este proyecto implementa estándares personalizados documentados en:
- [Documentación en Línea](https://docs-proyecto-final.vercel.app/)
- [`docs/standards/coding_standard/`](docs/standards/coding_standard/1_naming_conventions.md)

#### Requisitos del Estándar de Codificación

Todos los archivos Python deben cumplir estrictamente estas reglas, de lo contrario, el sistema rechazará el archivo y mostrará un mensaje de error:

1. **Contenido Mínimo**
   - Los archivos deben contener al menos una línea de código

2. **Requisitos de Nodos Padre**
   - Las siguientes estructuras deben contener contenido:
     ```python
     - Funciones
     - Clases
     - Métodos
     - Bloques if/elif/else
     - Bucles for
     - Bucles while
     - Bloques match/case
     - Bloques with
     - Bloques try/except/finally
     ```
     - ❌ `if condition: print()`
     - ❌ `for i in range(): print()`
     - ❌ `while(condition): i++`

3. **Una Declaración por Línea**
   - Se prohíben múltiples declaraciones por línea
   - ❌ `x = 6; y = 3`
   - ✅ `x = 6`
   - ✅ `y = 3`

4. **Sin Expresiones Anidadas**
   - Lo siguiente no puede anidarse:
     ```python
     - Operadores ternarios
     - Comprehensions de listas
     - Comprehensions de diccionarios
     - Comprehensions de conjuntos
     - Generators
     ```
    - ❌ `[x for x in [y for y in range(10)]]`
    - ❌ `a if b else (c if d else e)`
    - ❌ `{x: [y for y in range(x)] for x in range(5)}`

5. **Restricciones de Lambda**
   - No se permiten expresiones lambda
   - ❌ `lambda x: x + 1`

Por favor, consulte nuestra documentación [`docs/standards/coding_standard/`](docs/standards/coding_standard/1_naming_conventions.md) para información detallada sobre los estándares específicos implementados en esta herramienta.

### Almacenamiento

- Almacenamiento local basado en JSON
- Historial de métricas accesible
- Persistencia no volátil

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulte el archivo  [LICENSE](LICENSE) para más detalles.

Copyright (c) 2024 AMILCAR PEREZ CANTO

La Licencia MIT te permite:
- ✅ Uso comercial
- ✅ Modificación
- ✅ Distribución
- ✅ Uso privado