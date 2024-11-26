---
# src/proyecto_1/docs/requirements/system_core_documentation.md
title: Documentación Principal del Sistema
description: Documentación principal del sistema de conteo de líneas de código incluyendo requerimientos, estándares y exclusiones
---

## 1. Información General

| Campo | Valor |
|-------|-------|
| Proyecto | Sistema de Conteo de LOC |
| Versión | 1.0 |
| Autor | Amílcar Pérez |
| Fecha | 13/11/2024 |
| Estatus | En Desarrollo |
| Plataforma | Windows |
| Python | 3.8+ |

## 2. Componentes Principales

### 2.1 Funcionalidades Core
1. Lectura de Archivos
   - Input: archivo .py único
   - Validación de extensión y existencia
   - Manejo de errores claro y específico
   - No análisis sintáctico complejo

2. Conteo de Líneas
   - **Físicas**: 
     * Según estándar de conteo
     * Exclusión de comentarios, líneas vacías, docstrings
   - **Lógicas**: 
     * Según estándar de codificación
     * Estructuras permitidas:
       - Funciones (def)
       - Clases (class)
       - Control (if/elif/else, for, while)
       - Match/case (máx 5 casos)
       - Operadores ternarios
       - List/Dict/Set comprehensions
       - Generadores
   - No análisis semántico

4. Visualización
   ```
   | Archivo     | LOC Físicas | LOC Lógicas | Fecha Análisis      |
   |-------------|-------------|-------------|---------------------|
   | ejemplo.py  | 50          | 30          | 2024-11-13 15:30:00 |
   ```

### 2.2. Estándares del Sistema

| Estándar | Propósito | Documento |
|----------|-----------|-----------|
| Conteo | Define reglas para contar líneas | [Estándar de conteo](../../../../docs/standards/counting_standard.md) |
| Codificación | Define prácticas de programación | [Estándar de codificación](../../../../docs/standards/coding_standard/1_naming_conventions.md) |

3. Almacenamiento (JSON)
   ```json
   [
    {
     "nombre_archivo": "ejemplo.py",
     "loc_fisicas": 50,
     "loc_logicas": 30,
     "fecha_analisis": "2024-11-13 15:30:00"
    }
   ]
   ```

### 2.3 Restricciones Técnicas
- Solo Windows
- Python 3.8+
- Solo archivos .py individuales
- JSON como único almacenamiento
- Interface por línea de comandos
- Mensajes de error claros y específicos
- Documentación básica requerida

## 3. Flujo del Sistema

1. **Input**
   ```bash
   python loc_counter.py path/to/file.py
   ```
   - Validaciones:
     * Archivo existe
     * Extensión .py
     * Archivo legible

2. **Procesamiento**
   - Lectura línea por línea
   - Aplicación de reglas de conteo
   - Actualización/creación JSON
   - Manejo de errores en cada paso

3. **Output**
   - Tabla formateada con resultados
   - Mensajes de error específicos si ocurren
   - Confirmación de actualización JSON

## 4. Exclusiones Explícitas

1. **No Incluye**
   - Análisis sintáctico complejo
   - Análisis semántico
   - Procesamiento de carpetas
   - Otros formatos de archivo
   - Reportes especiales
   - Validación de código Python
   - Detección de código duplicado
   - Análisis de calidad
   - Formateo de código
   - Sugerencias de mejora

2. **Limitaciones**
   - Solo Windows
   - Un archivo a la vez
   - Sin interfaz gráfica
   - JSON simple (no BD)
   - Sin validación sintáctica profunda

## 5. Diseño del Sistema

### 5.1 Estructura de Directorios
```
src/
├── main.py                 # Entry point - command line interface
├── core/
│   ├── __init__.py
│   ├── lector_archivo.py     # Handles file reading and basic validation
│   ├── contador_logico.py # Implements logical LOC counting rules
│   └── almacenamiento_metricas.py    # Manages JSON storage and retrieval
├── models/
│   ├── __init__.py
│   └── metricas.py         # Data models for storing metricas and results
├── utils/
│   ├── __init__.py
│   ├── validators.py      # Input validation functions
│   └── formatters.py      # Output formatting utilities
└── tests/
    ├── __init__.py
    ├── test_file_reader.py
    ├── test_logical_counter.py
    └── test_json_handler.py
```

### 5.2 Descripción de Módulos y Relaciones

#### 5.2.1 Módulo Principal  
`main.py`  
- Punto de entrada para la aplicación.  
- Maneja los argumentos de línea de comandos.  
- Orquesta el flujo entre módulos.  
- Dependencias: core.lector_archivo, core.contador_logico, core.almacenamiento_metricas.  

#### 5.2.2 Módulos Core  
`core/lector_archivo.py`  
- Responsable de leer archivos Python.  
- Validación básica de archivos.  
- Retorna el contenido del archivo para su procesamiento.  
- Dependencias: utils.validators.  

`core/contador_logico.py`  
- Implementa reglas lógicas para el conteo de LOC (líneas de código lógico).  
- Procesa el contenido del archivo línea por línea.  
- Retorna un objeto de métricas.  
- Dependencias: models.metricas.  

`core/almacenamiento_metricas.py`  
- Administra el almacenamiento y recuperación en formato JSON.  
- Crea/actualiza el historial de métricas.  
- Dependencias: models.metricas.  

#### 5.2.3 Modelos  
`models/metricas.py`  
- Estructuras de datos para métricas.  
- Objetos inmutables para los resultados.  
- Sin dependencias.  

#### 5.2.4 Utilidades  
`utils/validators.py`  
- Funciones de validación de entradas.  
- Verificación de extensiones de archivo.  
- Validación de rutas.  
- Sin dependencias.  

`utils/formatters.py`  
- Utilidades para formateo de salida.  
- Generación de tablas para resultados.  
- Sin dependencias.  