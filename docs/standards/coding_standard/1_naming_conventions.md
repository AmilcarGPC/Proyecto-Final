---
# docs/standards/coding_standard/naming_conventions.md
title: Convenciones de Nombrado
description: Esta sección describe las convenciones de nombrado para variables, funciones, clases y constantes en Python. Incluye ejemplos y mejores prácticas.
---

Este documento establece las reglas fundamentales para nombrar elementos en código Python. El objetivo es mantener consistencia, legibilidad y facilitar el mantenimiento del código. Las convenciones cubren variables, funciones, clases y constantes, con énfasis en el uso de snake_case, nombres descriptivos en inglés y prácticas específicas para cada tipo de elemento.

## 1. Variables

### Instrucciones
- Usar snake_case para nombres de variables
- Nombres descriptivos pero concisos
- Evitar nombres de una sola letra excepto en loops
- Usar nombres en español
- Nombres deben ser sustantivos o frases nominales

### Mejores Prácticas
- Nombres que indiquen el propósito o contenido
- Evitar abreviaturas no estándar
- Prefijo 'es_' o 'tiene_' para booleanos
- Usar plural para colecciones
- Evitar nombres que se diferencien solo por mayúsculas

### Ejemplos
```python
# Correcto
nombre_usuario = "Juan"
esta_activo = True
contador_elementos = 42
lista_estudiantes = ["Ana", "Bob"]

# Incorrecto
userName = "Juan"  # camelCase
x = "Juan"        # no descriptivo
user = "Juan"     # inglés
```

### Verificación
- [ ] ¿Usa snake_case?
- [ ] ¿Es descriptivo?
- [ ] ¿Está en inglés?
- [ ] ¿Evita nombres de una letra?
- [ ] ¿Indica claramente el propósito?

## 2. Funciones

### Instrucciones
- Usar snake_case
- Nombres deben ser verbos o frases verbales
- Documentar parámetros con type hints
- Métodos mágicos limitados a __init__, __str__, __repr__
- Funciones estándar (main, init) en inglés

### Mejores Prácticas
- Nombres que describan la acción
- Máximo 30 caracteres
- Prefijos comunes: get_, set_, is_, has_, validate_
- Un solo propósito por función
- Evitar argumentos posicionales ambiguos

### Ejemplos
```python
# Correcto
def calcular_total(precios: list[float]) -> float:
    return sum(precios)

def es_usuario_valido(id_usuario: str) -> bool:
    return id_usuario.isalnum()

# Incorrecto
def calc(): # no descriptivo
def ProcessData(): # PascalCase y en inglés
```

### Verificación
- [ ] ¿Usa snake_case?
- [ ] ¿Es un verbo o frase verbal?
- [ ] ¿Tiene type hints?
- [ ] ¿Nombre menor a 30 caracteres?
- [ ] ¿Describe claramente la acción?

## 3. Clases

### Instrucciones
- Usar PascalCase
- Nombres deben ser sustantivos
- Sin prefijos o sufijos especiales
- Incluir docstring descriptivo

### Mejores Prácticas
- Nombres que representen entidades
- Una clase por archivo
- Evitar nombres genéricos
- Usar nombres singulares

### Ejemplos
```python
# Correcto
class CuentaUsuario:
    def __init__(self, nombre_usuario: str):
        self.nombre_usuario = nombre_usuario

class AnalizadorArchivo:
    """Maneja el análisis de diferentes formatos de archivo."""
    pass

# Incorrecto
class user_account: # snake_case y en inglés
class datos: # muy genérico
```

### Verificación
- [ ] ¿Usa PascalCase?
- [ ] ¿Es un sustantivo?
- [ ] ¿Tiene docstring?
- [ ] ¿Nombre descriptivo y específico?

## 4. Constantes

### Instrucciones
- Usar UPPER_SNAKE_CASE
- Definir al inicio del módulo
- Valores inmutables
- Nombres descriptivos

### Mejores Prácticas
- Agrupar constantes relacionadas
- Documentar unidades si aplica
- Evitar números mágicos en el código

### Ejemplos
```python
# Correcto
CONEXIONES_MAXIMAS = 100
TIEMPO_ESPERA_MS = 5000
URL_BASE_API = "https://api.ejemplo.com"

# Incorrecto
MaxConnections = 100 # PascalCase y en inglés
tiempo_espera = 5000 # no parece constante
```

### Verificación
- [ ] ¿Usa UPPER_SNAKE_CASE?
- [ ] ¿Está al inicio del módulo?
- [ ] ¿Valor inmutable?
- [ ] ¿Nombre descriptivo?