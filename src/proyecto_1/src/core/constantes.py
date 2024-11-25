"""
Nombre del módulo: constantes.py
Ruta: src/core/constantes.py
Descripción: Define constantes utilizadas en el análisis de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18/11/2024
Última Actualización: 18/11/2024

Dependencias:
    - models.nodes.NodeType

Uso:
    from core.constantes import CORCHETES, TIPOS_COMPREHENSION

    tipo = TIPOS_COMPREHENSION.get('[')
    cierre = CORCHETES.get('(')

Notas:
    - Mapea símbolos de apertura con sus correspondientes cierres
    - Define tipos de expresiones de comprensión según su símbolo
"""
from models.nodes import NodeType

# Mapeo de símbolos de apertura con sus correspondientes cierres
CORCHETES = {
    '[': ']',
    '(': ')',
    '{': '}'
}

# Mapeo de símbolos con tipos NodeType de expresiones de comprensión
TIPOS_COMPREHENSION = {
    '[': NodeType.LIST_COMPREHENSION,
    '{': NodeType.SET_COMPREHENSION,
    '(': NodeType.GENERATOR_EXPRESSION
}