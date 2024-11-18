---
# docs/standards/coding_standard/code_metrics.md
title: Métricas de Código
description: Esta sección define las métricas de código para evaluar la calidad y complejidad de funciones y clases en Python. Incluye ejemplos y recomendaciones.
---

Este documento establece métricas cuantitativas para evaluar la calidad del código Python.


## 1. Métricas de Función

### Instrucciones
- Máximo 20 líneas por función (excluyendo docstring)
- Máximo 3 parámetros por función
- Máximo 2 niveles de anidación
- Una función = una tarea

### Mejores Prácticas
- Usar nombres descriptivos que indiquen la acción
- Un solo return por función cuando sea posible
- Documentar parámetros con type hints
- Extraer lógica compleja a funciones auxiliares
- Evitar parámetros posicionales ambiguos

### Ejemplos
```python
# Correct - Simple function
def calculate_total(items: list[float], tax_rate: float) -> float:
    """Calculate total with tax."""
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)

# Wrong - Too many parameters
def process_order(items, tax_rate, discount, shipping, user, address, date):
    pass

# Wrong - Too many levels of nesting
def validate_data(data):
    for item in data:
        if item.is_valid:
            for field in item.fields:
                if field.type == "number":
                    if field.value > 0:
                        return True
    return False
```

### Verificación
- [ ] ¿Función ≤ 20 líneas?
- [ ] ¿≤ 3 parámetros?
- [ ] ¿≤ 2 niveles de anidación?
- [ ] ¿Nombre es un verbo o frase verbal?
- [ ] ¿Tiene type hints?

## 2. Métricas de Clase

### Instrucciones
- Máximo 5 métodos por clase
- Máximo 2 responsabilidades por clase
- Cada método máximo 20 líneas
- Nombres descriptivos obligatorios

### Mejores Prácticas
- Una clase = un propósito principal
- Métodos ordenados: primero públicos, luego privados
- Constructor simple y claro
- Evitar estado mutable cuando sea posible
- Properties para acceso controlado a atributos

### Ejemplos
```python
# Correct
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def get_display_name(self) -> str:
        return f"{self.name} ({self.email})"

    def validate(self) -> bool:
        return '@' in self.email

# Wrong - Too many methods
class DataProcessor:
    def process_a(self): pass
    def process_b(self): pass
    def process_c(self): pass
    def process_d(self): pass
    def process_e(self): pass
    def process_f(self): pass  # Limit of 5 methods exceeded
```

### Verificación
- [ ] ¿≤ 5 métodos por clase?
- [ ] ¿≤ 2 responsabilidades?
- [ ] ¿Cada método ≤ 20 líneas?
- [ ] ¿Nombre es un sustantivo?
- [ ] ¿Constructor documentado?

## 3. Duplicación de Código

### Instrucciones
- Prohibido duplicar más de 3 líneas de código
- Extraer código duplicado a funciones
- Usar herencia simple cuando sea apropiado

### Mejores Prácticas
- Extraer patrones comunes a funciones utilitarias
- Usar herencia simple para código compartido
- Mantener funciones utilitarias en módulos separados
- Documentar razón de duplicación si es necesaria
- Preferir composición sobre herencia

### Ejemplos
```python
# Correct - Reused code
def process_user(user):
    if user.active:
        user.last_login = datetime.now()
        user.login_count += 1
        user.save()

def process_users(users):
    for user in users:
        process_user(user)

def process_admins(admins):
    for admin in admins:
        process_user(admin)

# Wrong - Duplicated code
def process_users(users):
    for user in users:
        if user.active:
            user.last_login = datetime.now()
            user.login_count += 1
            user.save()

def process_admins(admins):
    for admin in admins:  # Duplicated code
        if admin.active:
            admin.last_login = datetime.now()
            admin.login_count += 1
            admin.save()
```

### Verificación
- [ ] ¿Sin bloques > 3 líneas duplicados?
- [ ] ¿Código común extraído a funciones?
- [ ] ¿Herencia usada apropiadamente?
- [ ] ¿Funciones utilitarias documentadas?
- [ ] ¿Sin copy-paste de código?