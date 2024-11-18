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
   - No se permiten múltiples párrafos
   - Un solo ejemplo por docstring
   - Usar solo plantillas definidas

3. **Vocabulario Permitido**
   Para descripciones, usar solo los siguientes verbos:
   - Calculates/Calculate
   - Processes/Process
   - Validates/Validate
   - Returns/Return
   - Gets/Get
   - Sets/Set
   - Creates/Create
   - Updates/Update
   - Deletes/Delete
   - Checks/Check


## 1. Docstrings para Módulos

### Instrucciones
Seguir el siguiente formato:
```python
"""
Module name: nombre_archivo.py
Ruta: [Ruta del archivo]
Description: [Descripción breve del propósito del módulo]
Project: [Nombre del proyecto al que pertenece]
Author: [Nombre del desarrollador principal]
Organization: Equipo 3
License: MIT
Date Created: AAAA-MM-DD
Last Update: AAAA-MM-DD

Dependencies:
    - [paquete] >= [versión]
    - [paquete] >= [versión]

Usage:
    [Instrucciones de cómo utilizar este módulo, optimizadas para su reutilización]

Notes:
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
# Correct
"""
Module name: open_file.py
Route: src/program1/open_file.py
Description: Opens a file and determines if it is a .py file.
Project: Physical and Logical Line Counting System in Python
Author: Ana Martínez
Organization: Equipo 3
License: MIT
Date Created: 16-11-2024
Last Update: 18-11-2024

Dependencies:
    - pandas >= 1.5.0
    - numpy >= 1.23.0
    - matplotlib >= 3.5.0

Usage:
    As module:
        from open_file import process_file.
        file = process_file(“file.csv”)

Notes:
    - Input files must be in .py format, otherwise an error will be displayed.
    - the module returns the file in txt format if it is .py
"""

# Wrong
"""
csv stuff - handles files and does things with them
made by john on 1/1/24
"""
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
# Correct
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers.

    Args:
        numbers (List[float]): List of numerical values to average.
            Must be non-empty list of integers or floats.

    Returns:
        float: The arithmetic mean of the input numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If any element is not a number.

    Example:
        >>> calculate_average([1.0, 2.0, 3.0])
        2.0
    """
    if not numbers:
        raise ValueError("List cannot be empty")
    return sum(numbers) / len(numbers)

# Wrong
def calc_avg(nums):
    """averages numbers"""
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
| **Methods** | Un método por línea con args, tipo retorno y descripción | `deposit(amount: float) -> None: Adds the specified amount to balance` |
| **Example** | 3 líneas máximo: instanciación, uso y salida | `>>> account = BankAccount("12345", "John Doe")`<br>`>>> account.deposit(100.0)`<br>`>>> account.balance`<br>`100.0` |

### Mejores Prácticas
- Separar atributos de métodos
- Documentar inicializador
- Mantener ejemplos simples
- Mencionar restricciones importantes
- Usar type hints para atributos

### Ejemplos
```python
# Correct
class BankAccount:
    """A class to represent a basic bank account.

    Handles basic operations like deposits and withdrawals while
    maintaining a current balance.

    Attributes:
        account_number (str): Unique identifier for the account
        balance (float): Current balance in the account
        owner (str): Name of the account holder

    Example:
        >>> account = BankAccount("12345", "John Doe")
        >>> account.deposit(100.0)
        >>> account.balance
        100.0
    """

    def __init__(self, account_number: str, owner: str):
        self.account_number = account_number
        self.owner = owner
        self.balance = 0.0

# Wrong
class Account:
    """handles money stuff"""
    def __init__(self, num, own):
        self.num = num
        self.own = own
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

### Mejores Prácticas
- Evitar comentarios obvios
- Actualizar cuando el código cambia
- Usar inglés consistentemente
- Mantener máximo 72 caracteres
- Comentar decisiones importantes

### Ejemplos
```python
# Correct
def process_data(data: list) -> list:
    # Skip first row as it contains headers
    filtered_data = data[1:]
    
    # Using 0.15 as threshold based on statistical analysis
    return [x for x in filtered_data if x > 0.15]

# Wrong
def process(d):
    f = d[1:]  # gets data
    return [x for x in f if x > 0.15]  # returns filtered
```

### Verificación
- [ ] ¿Comentarios necesarios?
- [ ] ¿Explican el "por qué"?
- [ ] ¿Concisos y claros?
- [ ] ¿Bien formateados?