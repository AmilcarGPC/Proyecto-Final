---
# docs/standards/coding_standard/code_format.md
title: Formato del Código
description: Esta sección describe las reglas de formato para el código Python. Incluye guías rápidas y ejemplos.
---

Este documento define las reglas estándar de formato para código Python, enfocándose en la consistencia y legibilidad. Se cubren aspectos como indentación, espaciado y estructura del código, siguiendo las mejores prácticas.


## 1. Indentación

### Instrucciones
- Usar exactamente 4 espacios por nivel de indentación
- No usar tabulaciones
- Mantener consistencia en todo el código
- Alinear elementos multilínea con el primer carácter

### Mejores Prácticas
- Configurar el editor para convertir tabs a espacios
- Mantener un máximo de 3 niveles de indentación
- Usar indentación vertical para mejorar legibilidad
- Evitar líneas en blanco con espacios

### Ejemplos
```python
# Correct
def my_function():
    if condition:
        do_something()
        for item in items:
            process(item)

# Wrong
def my_function():
  if condition:    # 2 spaces
        do_something()    # indentation mixing
```

### Verificación
- [ ] ¿Usa 4 espacios exactos?
- [ ] ¿No hay tabulaciones?
- [ ] ¿Mantiene consistencia?
- [ ] ¿Máximo 3 niveles?

## 2. Longitud Máxima de Línea

### Instrucciones
- Límite estricto de 80 caracteres por línea
- 72 caracteres para comentarios/docstrings
- Usar paréntesis para continuación de líneas
- Romper líneas antes de operadores

### Mejores Prácticas
- Usar paréntesis para dividir expresiones largas
- Alinear elementos en múltiples líneas
- Preferir legibilidad sobre brevedad
- Mantener argumentos de funciones alineados

### Ejemplos
```python
# Correct
long_function_name(
    parameter1, parameter2,
    parameter3, parameter4
)

total = (first_variable
         + second_variable
         + third_variable)

# Wrong
long_function_name(parameter1, parameter2, parameter3, parameter4)  # > 80 chars

total = first_variable + second_variable + third_variable  # > 80 chars
```

### Verificación
- [ ] ¿Líneas <= 80 caracteres?
- [ ] ¿Comentarios <= 72 caracteres?
- [ ] ¿Usa paréntesis para continuación?
- [ ] ¿Alineación correcta?

## 3. Espacios en Blanco

### Instrucciones
- Un espacio después de coma
- No espacios antes de coma/punto y coma
- No espacios dentro de paréntesis/corchetes
- Un espacio alrededor de operadores
- Dos líneas en blanco entre funciones de alto nivel

### Mejores Prácticas
- No espacios al final de líneas
- Una línea en blanco entre métodos de clase
- No espacios antes de paréntesis en llamadas
- Espacio después de # en comentarios

### Ejemplos
```python
# Correct
x = 1
y = 2

def function1():
    pass


def function2():
    pass

# Wrong
x=1
y=2
def function1() :
    pass
def function2():
    pass
```

### Verificación
- [ ] ¿Espaciado correcto en operadores?
- [ ] ¿Espaciado correcto en comas?
- [ ] ¿Líneas en blanco apropiadas?
- [ ] ¿Sin espacios al final?

## 4. Saltos de Línea

### Instrucciones
- Dos líneas en blanco entre funciones de alto nivel
- Una línea en blanco entre métodos de clase
- Una línea en blanco entre bloques lógicos
- No líneas en blanco excesivas

### Mejores Prácticas
- Agrupar código relacionado
- Usar saltos para mejorar legibilidad
- Mantener consistencia en todo el archivo
- Eliminar líneas en blanco duplicadas

### Ejemplos
```python
class MyClass:
    def method1(self):
        return True

    def method2(self):
        return False


def top_level_function():
    pass


def another_function():
    pass
```

### Verificación
- [ ] ¿Dos líneas entre funciones top-level?
- [ ] ¿Una línea entre métodos?
- [ ] ¿Bloques lógicos separados?
- [ ] ¿Sin líneas excesivas?

## 5. Uso de Paréntesis

### Instrucciones
- Usar paréntesis para claridad
- No usar paréntesis innecesarios
- Paréntesis para continuación de líneas
- Mantener consistencia en expresiones

### Mejores Prácticas
- Usar para operaciones complejas
- Alinear paréntesis de cierre
- Mantener legibilidad
- Evitar anidación excesiva

### Ejemplos
```python
# Correct
if (long_condition_a and 
    long_condition_b):
    pass

result = (value_one
          + value_two
          + value_three)

# Wrong
if (x == 1):  # unnecessary parentheses
    pass
```

### Verificación
- [ ] ¿Uso necesario de paréntesis?
- [ ] ¿Alineación correcta?
- [ ] ¿Expresiones claras?
- [ ] ¿Sin anidación excesiva?