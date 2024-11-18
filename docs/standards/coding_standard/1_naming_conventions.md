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
- Usar nombres en inglés
- Nombres deben ser sustantivos o frases nominales

### Mejores Prácticas
- Nombres que indiquen el propósito o contenido
- Evitar abreviaturas no estándar
- Prefijo 'is_' o 'has_' para booleanos
- Usar plural para colecciones
- Evitar nombres que se diferencien solo por mayúsculas

### Ejemplos
```python
# Correct
user_name = "John"
is_active = True
items_count = 42
students_list = ["Ana", "Bob"]

# Wrong
userName = "John"  # camelCase
x = "John"        # no descriptive
Usuario = "John"  # Spanish
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
- Máximo 30 caracteres
- Documentar parámetros con type hints
- Métodos mágicos limitados a __init__, __str__, __repr__

### Mejores Prácticas
- Nombres que describan la acción
- Prefijos comunes: get_, set_, is_, has_, validate_
- Un solo propósito por función
- Evitar argumentos posicionales ambiguos

### Ejemplos
```python
# Correct
def calculate_total(prices: list[float]) -> float:
    return sum(prices)

def is_valid_user(user_id: str) -> bool:
    return user_id.isalnum()

# Wrong
def calc(): # no descriptive
def ProcessData(): # PascalCase
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
# Correct
class UserAccount:
    def __init__(self, username: str):
        self.username = username

class FileParser:
    """Handles parsing of different file formats."""
    pass

# Wrong
class user_account: # snake_case
class data: # too generic
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
# Correct
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT_MS = 5000
API_BASE_URL = "https://api.example.com"

# Wrong
MaxConnections = 100 # PascalCase
timeout = 5000 # not constant-like
```

### Verificación
- [ ] ¿Usa UPPER_SNAKE_CASE?
- [ ] ¿Está al inicio del módulo?
- [ ] ¿Valor inmutable?
- [ ] ¿Nombre descriptivo?