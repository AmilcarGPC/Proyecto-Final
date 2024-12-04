"""
Nombre del módulo: node_types.py
Ruta: src/config/node_types.py
Descripción: Define los conjuntos de tipos de nodos permitidos para el análisis \
de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - models.nodos.TipoNodo

Uso:
    from config.node_types import PARENT_NODE_TYPES, LOGICAL_NODE_TYPES

Notas:
    - Utiliza los tipos de nodos definidos para el árbol de análisis de código \
    Python
"""

from analizador_cambios.models.nodos import TipoNodo # AÑADIDA EN UN 0.83%

# Tipos de nodos que pueden contener otros nodos
PARENT_NODE_TYPES = {
    TipoNodo.ROOT,
    TipoNodo.FUNCTION, 
    TipoNodo.CLASS, 
    TipoNodo.METHOD,
    TipoNodo.IF, 
    TipoNodo.ELIF, 
    TipoNodo.ELSE, 
    TipoNodo.FOR, 
    TipoNodo.WHILE, 
    TipoNodo.MATCH, 
    TipoNodo.CASE,
    TipoNodo.WITH,
    TipoNodo.TRY,
    TipoNodo.EXCEPT,
    TipoNodo.FINALLY
}

# Tipos de nodos considerados como estructuras lógicas
LOGICAL_NODE_TYPES = {
    TipoNodo.FUNCTION,
    TipoNodo.METHOD,
    TipoNodo.CLASS,
    TipoNodo.IF,
    TipoNodo.FOR,
    TipoNodo.WHILE,
    TipoNodo.MATCH,
    TipoNodo.LIST_COMPREHENSION,
    TipoNodo.DICT_COMPREHENSION,
    TipoNodo.SET_COMPREHENSION,
    TipoNodo.GENERATOR_EXPRESSION,
    TipoNodo.TERNARY,
    TipoNodo.WITH,
    TipoNodo.TRY,
    TipoNodo.PROPERTY,
    TipoNodo.DECORATOR,
}

# Tipos de nodos que el estándar no permite anidar
NO_NESTED_ALLOWED = {
    TipoNodo.TERNARY,
    TipoNodo.LIST_COMPREHENSION,
    TipoNodo.DICT_COMPREHENSION,
    TipoNodo.SET_COMPREHENSION,
    TipoNodo.GENERATOR_EXPRESSION
}

# Tipos de nodos especificos para comentarios y documentación
COMMENT_NODE_TYPES = {
    TipoNodo.MODULE_DOCSTRING,
    TipoNodo.FUNCTION_DOCSTRING,
    TipoNodo.CLASS_DOCSTRING,
    TipoNodo.COMMENT,
    TipoNodo.INLINE_COMMENT
}

# Tipos de nodos que representan código válido para contar líneas físicas
VALID_CODE_NODE_TYPES = {
    TipoNodo.FUNCTION,
    TipoNodo.CLASS,
    TipoNodo.IF,
    TipoNodo.ELIF,
    TipoNodo.ELSE,
    TipoNodo.FOR,
    TipoNodo.WHILE,
    TipoNodo.MATCH,
    TipoNodo.CASE,
    TipoNodo.EXPRESSION,
    TipoNodo.LIST_COMPREHENSION,
    TipoNodo.DICT_COMPREHENSION,
    TipoNodo.SET_COMPREHENSION,
    TipoNodo.GENERATOR_EXPRESSION,
    TipoNodo.TERNARY,
    TipoNodo.WITH,
    TipoNodo.TRY,
    TipoNodo.EXCEPT,
    TipoNodo.FINALLY,
    TipoNodo.CONSTANT,
    TipoNodo.METHOD,
    TipoNodo.PROPERTY,
    TipoNodo.DECORATOR,
    TipoNodo.RETURN,
    TipoNodo.BREAK,
    TipoNodo.CONTINUE,
    TipoNodo.RAISE,
    TipoNodo.ASSERT
}
