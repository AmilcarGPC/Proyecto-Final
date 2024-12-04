---
# docs/estandares/estandar_conteo.md
title: Estándar de Conteo
description: Este documento describe las reglas y guías para contar líneas de código en Python.
---

## 1. Información General

| Campo | Valor | Notas |
|-------|-------|-------|
| Tipos de conteo | Físico y Lógico | Se soportan ambos tipos de conteo |
| Versión | 1.2 | Incluye conteo lógico |
| Última actualización | 24-11-2024 |  |
| Herramientas recomendadas | Tarea 1 | Para conteo automático |

### 1.1 Estructuras Lógicas

Para el conteo lógico, se consideran como estructuras independientes:

- Definiciones de funciones y métodos
- Definiciones de clases 
- Estructuras `if` (`elif` y `else` no son consideradas independientes)
- Bucles `for` y `while`
- Expresiones `match` (`case` no es considerada independientes)
- Comprensiones (`list`, `dict`, `set`)
- Expresiones generadoras
- Operadores ternarios
- Bloques `with`
- Bloques `try` (`except` y `finally` no son consideradas independientes)
- Propiedades (`@property`)
- Decoradores (`@`)

Cada estructura lógica cuenta como una unidad, sin importar su extensión física en líneas de código.

## 2. Reglas de Conteo por Tipo de Sentencia

| Tipo de Sentencia | Incluir | LOC | Comentarios |
|-------------------|---------|-----|-------------|
| **Imports** |
| Import simple | Sí | 1 | `import libreria` |
| Import múltiple | Sí | N | `import pandas, pyqt5` cuenta como N imports |
| From import | Sí | 1 | `from module import a,b,c` cuenta como 1 |
| **Comentarios** |
| Comentarios en línea | No | 0 | `# comentario` |
| Comentarios con código | Solo el código | 1 | `print("hola") # comentario` |
| Docstrings | No | 0 | Comentarios multi-línea no cuentan |
| **Código** |
| Asignaciones simples | Sí | 1 | Una instrucción por línea |
| Asignaciones multiples | Sí | N | `x, y, z = 1, 2, 3  # 3 LOC` |
| Líneas vacías | No | 0 | Espacios en blanco no cuentan |
| **Estructuras de Control** |
| Definición de función | Sí | 1 | `def funcion():` |
| Definición de clase | Sí | 1 | `class MiClase:` |
| If/Elif/Else | Sí | 1 | Cada línea cuenta independientemente |
| Bucles (for/while) | Sí | 1 | La declaración del bucle |
| Pass statements | Sí | 1 | `pass` cuenta como línea válida |
| Try/Except/Finally        | Sí      | 1 por bloque | Cada bloque cuenta como línea separada.<br><br> try: <br> x = 1 / 0  # 1 LOC <br> except <br> ZeroDivisionError: <br> print("Error")  # 1 LOC <br> finally: <br> print("Fin del bloque")  # 1 LOC                    |
| With statements         | Sí          | 1        | `with open("archivo.txt", "r") as f:` |
| Generadores y comprehensions | Sí    | 1 | Cada línea de la expresión cuenta.            |
| Decoradores        | Sí     | 1 | `@decorator` |

## 3. Casos Especiales

| Caso                     | Conteo        | Ejemplo/Comentarios                                                                 |
|--------------------------|---------------|------------------------------------------------------------------------------------|
| **Asignaciones Multilínea** |               |                                                                                    |
| Listas/Diccionarios | 1  | checkboxes = [<br>    self.checkbox1,    *# 1 LOC*<br>    self.checkbox2,<br>    self.checkbox3<br>] |
| Comprehensions | 1 | results = [<br>    x * 2    *# 1 LOC*<br>    for x in range(10)   <br>] |
| Generadores | 1 | results = (<br>    x * 2    *# 1 LOC*<br>    for x in range(10)   <br>) |
| Operaciones    | 1   | resultado = (x + y +   *# 1 LOC total*<br>            z + 5)        |
| Strings        | 1   | mensaje = "Este es un mensaje \ *# 1 LOC*<br>    muy largo que continúa \ <br> en múltiples líneas" |


## 4. Reglas Adicionales

1. **Continuación de línea explícita:**
   - Cada línea física separada por `\` cuenta como 1 LOC
   - Ejemplo:
     ```python
     resultado = valor1 + \   # 1 LOC
                valor2
     ```

2. **Paréntesis implícitos:**
   - Cada línea dentro de paréntesis/corchetes/llaves cuenta como 1 LOC
   - Ejemplo:
     ```python
     mi_tupla = (
         valor1,          # 1 LOC total
         valor2,
         valor3
     )
     ```

3. **Funciones/Métodos:**
   - La línea de definición cuenta como 1 LOC
   - El cuerpo se cuenta línea por línea

## 5. Exclusiones
❌ Líneas vacías o espacios en blanco <br>
❌ Líneas de shebang o encoding <br>
❌ Docstrings de módulos al inicio del archivo <br>