"""
Nombre del módulo: constantes.py
Ruta: src/core/constantes.py
Descripción: Define constantes utilizadas en el análisis de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - models.nodos.TipoNodo

Uso:
    from core.constantes import CORCHETES, TIPOS_COMPREHENSION

    tipo = TIPOS_COMPREHENSION.get('[')
    cierre = CORCHETES.get('(')

Notas:
    - Mapea símbolos de apertura con sus correspondientes cierres
    - Define tipos de expresiones de comprensión según su símbolo
"""

from lineas_por_clase.models.nodos import TipoNodo

# Mapeo de símbolos de apertura con sus correspondientes cierres
CORCHETES = {
    '[': ']',
    '(': ')',
    '{': '}'
}

# Mapeo de símbolos con tipos TipoNodo de expresiones de comprensión
TIPOS_COMPREHENSION = {
    '[': TipoNodo.LIST_COMPREHENSION,
    '{': TipoNodo.SET_COMPREHENSION,
    '(': TipoNodo.GENERATOR_EXPRESSION
}