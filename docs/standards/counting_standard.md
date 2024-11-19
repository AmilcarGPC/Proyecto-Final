---
# docs/standards/counting_standard.md
title: Estándar de Conteo de LOC para Python
description: Este documento describe las reglas y guías para contar líneas de código en Python.
---

## 1. Información General

| Campo | Valor | Notas |
|-------|-------|-------|
| Tipo de conteo | Físico | Se cuenta cada línea física independientemente |
| Versión | 1.1 | Incluye guías rápidas y checklists |
| Última actualización | 16/11/2024 |  |
| Herramientas recomendadas | Tarea 1 | Para conteo automático |

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
| Declaraciones simples | Sí | 1 | Una instrucción por línea |
| Declaraciones múltiples | Sí | N | Una línea con múltiples instrucciones cuenta como N |
| Líneas vacías | No | 0 | Espacios en blanco no cuentan |
| Asignaciones multiples | Sí | N | `x, y, z = 1, 2, 3  # 3 LOC` |
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
| **Declaraciones Multilínea** |               |                                                                                    |
| Listas/Diccionarios multilínea | 1 por línea   | checkboxes = [<br>    self.checkbox1,    *# 4 LOC total*<br>    self.checkbox2,<br>    self.checkbox3<br>] |
| Operaciones multilínea    | 1 por línea   | resultado = (x + y +   *# 2 LOC total*<br>            z + 5)        |
| Strings multilínea        | 1 por línea   | Cada línea física dentro del string cuenta                                        |


## 4. Reglas Adicionales

1. **Continuación de línea explícita:**
   - Cada línea física separada por `\` cuenta como 1 LOC
   - Ejemplo:
     ```python
     resultado = valor1 + \   # 2 LOC
                valor2
     ```

2. **Paréntesis implícitos:**
   - Cada línea dentro de paréntesis/corchetes/llaves cuenta como 1 LOC
   - Ejemplo:
     ```python
     mi_tupla = (
         valor1,          # 4 LOC total
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
❌ Lineas auto-generadas <br>
❌ Docstrings de módulos al inicio del archivo <br>
❌ Cabeceras de licencia <br>