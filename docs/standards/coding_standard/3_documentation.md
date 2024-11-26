---
# docs/standards/coding_standard/documentation.md
title: Documentación
description: Esta sección describe las reglas y mejores prácticas para documentar módulos, funciones y clases en Python. Incluye ejemplos y recomendaciones.
---

Este documento establece los estándares de documentación para el código Python, incluyendo docstrings, comentarios y documentación externa. Se enfoca en mantener documentación clara, actualizada y útil siguiendo un estilo constante y propio de la organización.

### Reglas Generales de Documentación y Restricciones de Formato
1. **Longitud Máxima**
   - Docstrings: 5 líneas por función/método
   - Ejemplos: 3 líneas máximo
   - Descripciones: 1 línea por elemento

2. **Estructura**
   - Las comillas triples de apertura y cierre de un docstring deben estar solas en su línea
   - No se permiten múltiples párrafos
   - Un solo ejemplo por docstring
   - Usar solo plantillas definidas

3. **Vocabulario Permitido**
   Para descripciones, usar solo los siguientes verbos:
   - Calcula/Calcular
   - Procesa/Procesar
   - Valida/Validar
   - Retorna/Retornar
   - Obtiene/Obtener
   - Establece/Establecer
   - Crea/Crear
   - Actualiza/Actualizar
   - Elimina/Eliminar
   - Verifica/Verificar


## 1. Docstrings para Módulos

### Instrucciones
Seguir el siguiente formato:
```python
"""
Nombre del módulo: nombre_archivo.py
Ruta: [Ruta del archivo]
Descripción: [Descripción breve del propósito del módulo]
Proyecto: [Nombre del proyecto al que pertenece]
Autor: [Nombre del desarrollador principal]
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: AAAA-MM-DD
Última Actualización: AAAA-MM-DD

Dependencias:
    - [paquete] >= [versión (opcional)]
    - [paquete] >= [versión (opcional)]

Uso:
    [Instrucciones de cómo utilizar este módulo, optimizadas para su reutilización]

Notas (opcional):
    [Información adicional importante]
"""
```
| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Nombre del Módulo** | Usar nombre exacto .py en snake_case | `open_file.py` |
| **Ruta** | Ruta relativa desde directorio del proyecto | `src/program1/open_file.py` |
| **Descripción** | Explicación clara y concisa (máx 2 líneas) | "Procesa archivos y verifica que sean .py" |
| **Proyecto** | Nombre oficial del sistema | "Sistema de Conteo de Líneas Físicas y Lógicas en Python" |
| **Autor** | Nombre Apellido del desarrollador principal | "Ana Martínez" |
| **Organización** | Nombre estándar del equipo | "Equipo 3" |
| **Licencia** | Tipo de licencia estándar | "MIT" |
| **Fechas** | Creación y última actualización (DD-MM-AAAA) | Creación: 01-01-2024<br>Actualización: 15-01-2024 |
| **Dependencias** | Paquetes externos con versión mínima | `- pandas >= 1.5.0`<br>`- numpy >= 1.23.0` |
| **Uso** | Instrucciones de importación y ejecución | `from modulo import función`<br>`python archivo.py arg1 arg2` |
| **Notas** | Información adicional relevante | "Limitaciones conocidas..." |

### Mejores Prácticas
- Mantener el encabezado actualizado
- Ser conciso pero informativo
- Usar español en todo el encabezado
- Verificar la ortografía y gramática
- Mantener el formato consistente

### Ejemplos
```python
# Correcto
"""
Nombre del módulo: abrir_archivo.py
Ruta: src/programa1/abrir_archivo.py
Descripción: Abre un archivo y determina si es un archivo .py
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Ana Martínez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 16-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - pandas >= 1.5.0
    - numpy >= 1.23.0
    - matplotlib >= 3.5.0

Uso:
    Como módulo:
        from abrir_archivo import procesar_archivo
        archivo = procesar_archivo("archivo.csv")

Notas:
    - Los archivos de entrada deben estar en formato .py
    - El módulo retorna el archivo en formato txt si es .py
"""

import pandas as pd
# Incorrecto
"""
cosas de archivos - maneja archivos y hace cosas
hecho por pepe el 1/1/24
version 1.0
"""

import pandas as pd
```

### Verificación
- [ ] ¿Todos los campos están completos?
- [ ] ¿Las fechas están actualizadas?
- [ ] ¿Las dependencias están correctamente especificadas?
- [ ] ¿La información de uso está clara y actualizada?
- [ ] ¿Las notas son relevantes y útiles?

## 2. Docstrings para Funciones

### Instrucciones
Seguir el siguiente formato:
```python
"""
[Descripción de una línea]

Args:
    arg1 (type): [Descripción]

Returns:
    type: [Descripción]

Raises:
    Exception: [Descripción]

Example:
    >>> [Código]
    [Salida esperada]
"""
```

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **[Descripción]** | Breve descripción de una línea explicando qué hace la función | `Calculate the average of a list of numbers` |
| **Args** | Un argumento por línea, con tipo, descripción y alguna restricción | `numbers (List[float]): List of numerical values to average. Must be non-empty list of integers or floats.` |
| **Returns** | Tipo de retorno y descripción en 1 línea | `float: The arithmetic mean of the input numbers.` |
| **Raises** | Una excepción por línea con descripción | `ValueError: If the list is empty` |
| **Example** | Código de ejemplo (max 3 líneas) y salida | `>>> calculate_average([1.0, 2.0, 3.0])`<br>`2.0` |

### Mejores Prácticas
- Usar formato consistente
- Mantener primera línea concisa
- Documentar efectos secundarios
- Incluir precondiciones importantes
- Usar type hints básicos

### Ejemplos
```python
# Correcto
def calcular_promedio(numeros: list[float]) -> float:
    """
    Calcula el promedio de una lista de números.

    Args:
        numeros (List[float]): Lista de valores numéricos para promediar.
            Debe ser una lista no vacía de enteros o flotantes.

    Returns:
        float: La media aritmética de los números de entrada.

    Raises:
        ValueError: Si la lista está vacía.
        TypeError: Si algún elemento no es un número.

    Example:
        >>> calcular_promedio([1.0, 2.0, 3.0])
        2.0
    """
    if not numeros:
        raise ValueError("La lista no puede estar vacía")
    return sum(numeros) / len(numeros)

# Incorrecto
def calc_prom(nums):
    """hace el promedio"""
    return sum(nums)/len(nums)
```

### Verificación
- [ ] ¿Describe funcionalidad clara?
- [ ] ¿Documenta parámetros y tipos?
- [ ] ¿Especifica excepciones?
- [ ] ¿Incluye ejemplos?

## 3. Docstrings para Clases

### Instrucciones
Seguir el siguiente formato:
```python
"""
[Descripción breve de una línea]

[Descripción detallada de funcionalidad, máximo 2 líneas]

Attributes:
    [atributo] ([tipo]): [Descripción en una línea]
    [atributo] ([tipo]): [Descripción en una línea]
    
Methods:
    [método]([args]) -> [return_type]: [Descripción en una línea]
    [método]([args]) -> [return_type]: [Descripción en una línea]

Example:
    >>> [Código de instanciación]
    >>> [Código de uso de método]
    [Salida esperada]
"""
```
| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **[Descripción breve]** | Propósito de la clase en una línea | `A class to represent a basic bank account` |
| **[Descripción detallada]** | Explicación de funcionalidad (max 2 líneas) | `Handles basic operations like deposits and withdrawals while maintaining a current balance` |
| **Attributes** | Un atributo por línea con tipo y descripción | `balance (float): Current balance in the account` |
| **Methods** | Un método (público) por línea con args, tipo retorno y descripción | `deposit(amount: float) -> None: Adds the specified amount to balance` |
| **Example** | 3 líneas máximo: instanciación, uso y salida | `>>> account = BankAccount("12345", "John Doe")`<br>`>>> account.deposit(100.0)`<br>`>>> account.balance`<br>`100.0` |

### Mejores Prácticas
- Separar atributos de métodos
- Documentar inicializador
- Mantener ejemplos simples
- Mencionar restricciones importantes
- Usar type hints para atributos

### Ejemplos
```python
# Correcto
class CuentaBancaria:
    """
    Una clase para representar una cuenta bancaria básica.

    Maneja operaciones básicas como depósitos y retiros mientras
    mantiene un saldo actual.

    Attributes:
        numero_cuenta (str): Identificador único de la cuenta
        saldo (float): Saldo actual en la cuenta
        propietario (str): Nombre del titular de la cuenta

    Example:
        >>> cuenta = CuentaBancaria("12345", "Juan Pérez")
        >>> cuenta.depositar(100.0)
        >>> cuenta.saldo
        100.0
    """

    def __init__(self, numero_cuenta: str, propietario: str):
        self.numero_cuenta = numero_cuenta
        self.propietario = propietario
        self.saldo = 0.0

# Incorrecto
class Cuenta:
    """maneja dinero y esas cosas"""
    def __init__(self, num, prop):
        self.num = num
        self.prop = prop
```

### Verificación
- [ ] ¿Describe propósito de clase?
- [ ] ¿Documenta atributos?
- [ ] ¿Lista métodos principales?
- [ ] ¿Incluye ejemplo de uso?

## 4. Comentarios en Línea

### Instrucciones
- Usar solo cuando el código no es auto-explicativo
- Mantener comentarios concisos
- Explicar el "por qué" no el "qué"
- Mantener el mismo nivel de indentación
- Usar # seguido de un espacio
- Evitar los docstrings como comentarios en línea usando ; """ o ; ''' 

### Mejores Prácticas
- Evitar comentarios obvios
- Actualizar cuando el código cambia
- Usar español consistentemente
- Mantener máximo 72 caracteres
- Comentar decisiones importantes

### Ejemplos
```python
# Correct
def procesar_datos(datos: list) -> list:
    # Omitir primera fila ya que contiene encabezados
    datos_filtrados = datos[1:]
    
    # Usando 0.15 como umbral basado en análisis estadístico
    return [x for x in datos_filtrados if x > 0.15]

esta_listo = True # Flag definido por DRS-123...

# Incorrecto
def procesar(d):
    f = d[1:]  # obtiene datos
    return [x for x in f if x > 0.15]  # filtra cosas

esta_activo = True; """ Flag definido por DRS-123... """
```

### Verificación
- [ ] ¿Comentarios necesarios?
- [ ] ¿Explican el "por qué"?
- [ ] ¿Concisos y claros?
- [ ] ¿Bien formateados?