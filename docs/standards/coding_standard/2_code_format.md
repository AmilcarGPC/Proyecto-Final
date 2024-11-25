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
- Usar indentación vertical para mejorar legibilidad
- Evitar líneas en blanco con espacios

### Ejemplos
```python
# Correcto
def mi_funcion():
    if condicion:
        hacer_algo()
        for elemento in elementos:
            procesar(elemento)

# Incorrecto
def mi_funcion():
  if condicion:    # 2 espacios
        hacer_algo()    # mezcla de identaciones
```

### Verificación
- [ ] ¿Usa 4 espacios exactos?
- [ ] ¿No hay tabulaciones?
- [ ] ¿Mantiene consistencia?
- [ ] ¿Máximo 3 niveles?

## 2. Características de una Línea

### Instrucciones
- Límite estricto de 80 caracteres por línea
- Usar paréntesis para continuación de líneas o \ al final
- Romper líneas antes de operadores
- No usar punto y coma (;) para combinar múltiples instrucciones

### Mejores Prácticas
- Usar paréntesis para dividir expresiones largas
- Alinear elementos en múltiples líneas
- Preferir legibilidad sobre brevedad
- Mantener argumentos de funciones alineados

### Ejemplos
```python
# Correcto
nombre_funcion_larga(parametro1, parametro2, parametro3,
    parametro4
)

total = primera_variable + \
        segunda_variable + \
        tercera_variable

a = 1
b = 2

# Incorrecto
nombre_funcion_larga(parametro1, parametro2, parametro3, parametro4, parametro5, parametro6)  # > 80 chars

total = primera_variable + segunda_variable + tercera_variable + cuarta_variable  # > 80 chars

a = 1; b = 2  # múltiples instrucciones en una línea
```

### Verificación
- [ ] ¿Líneas <= 80 caracteres?
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
# Correcto
x = 1
y = 2

def funcion1():
    pass


def funcion2():
    pass

lista = [1, 2, 3]
diccionario = {'a': 1, 'b': 2}

# Incorrecto
x=1
y=2
def funcion1() :
    pass
def funcion2():
    pass

lista=[1,2,3]
diccionario={'a':1,'b':2}
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
# Correcto
class MiClase:
    def metodo1(self):
        return True

    def metodo2(self):
        return False


def funcion_alto_nivel():
    pass


def otra_funcion():
    pass

# Incorrecto
class MiClase:
    def metodo1(self):
        return True
    def metodo2(self):    # falta línea en blanco
        return False
def funcion_alto_nivel():    # faltan dos líneas en blanco
    pass
def otra_funcion():    # faltan dos líneas en blanco
    pass
```

### Verificación
- [ ] ¿Dos líneas entre funciones top-level?
- [ ] ¿Una línea entre métodos?
- [ ] ¿Bloques lógicos separados?
- [ ] ¿Sin líneas excesivas?