"""
Nombre del módulo: node_types.py
Ruta: src/config/node_types.py
Descripción: Define los conjuntos de tipos de nodos permitidos para el análisis de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18/11/2024
Última Actualización: 18/11/2024

Dependencias:
    - models.nodes.NodeType

Uso:
    from config.node_types import PARENT_NODE_TYPES, LOGICAL_NODE_TYPES

Notas:
    - Utiliza los tipos de nodos definidos para el árbol de análisis de código Python
"""
from models.nodes import NodeType

# Tipos de nodos que pueden contener otros nodos
PARENT_NODE_TYPES = {
    NodeType.ROOT,
    NodeType.FUNCTION, 
    NodeType.CLASS, 
    NodeType.METHOD,
    NodeType.IF, 
    NodeType.ELIF, 
    NodeType.ELSE, 
    NodeType.FOR, 
    NodeType.WHILE, 
    NodeType.MATCH, 
    NodeType.CASE,
    NodeType.WITH,
    NodeType.TRY,
    NodeType.EXCEPT,
    NodeType.FINALLY
}

# Tipos de nodos considerados como estructuras lógicas
LOGICAL_NODE_TYPES = {
    NodeType.FUNCTION,
    NodeType.METHOD,
    NodeType.CLASS,
    NodeType.IF,
    NodeType.FOR,
    NodeType.WHILE,
    NodeType.MATCH,
    NodeType.LIST_COMPREHENSION,
    NodeType.DICT_COMPREHENSION,
    NodeType.SET_COMPREHENSION,
    NodeType.GENERATOR_EXPRESSION,
    NodeType.TERNARY,
    NodeType.WITH,
    NodeType.TRY,
    NodeType.PROPERTY,
    NodeType.DECORATOR,
}

# Tipos de nodos que el estándar no permite anidar
NO_NESTED_ALLOWED = {
    NodeType.TERNARY,
    NodeType.LIST_COMPREHENSION,
    NodeType.DICT_COMPREHENSION,
    NodeType.SET_COMPREHENSION,
    NodeType.GENERATOR_EXPRESSION
}

# Tipos de nodos especificos para comentarios y documentación
COMMENT_NODE_TYPES = {
    NodeType.MODULE_DOCSTRING,
    NodeType.FUNCTION_DOCSTRING,
    NodeType.CLASS_DOCSTRING,
    NodeType.COMMENT,
    NodeType.INLINE_COMMENT
}

# Tipos de nodos que representan código válido para contar líneas físicas
VALID_CODE_NODE_TYPES = {
    NodeType.FUNCTION,
    NodeType.CLASS,
    NodeType.IF,
    NodeType.ELIF,
    NodeType.ELSE,
    NodeType.FOR,
    NodeType.WHILE,
    NodeType.MATCH,
    NodeType.CASE,
    NodeType.EXPRESSION,
    NodeType.LIST_COMPREHENSION,
    NodeType.DICT_COMPREHENSION,
    NodeType.SET_COMPREHENSION,
    NodeType.GENERATOR_EXPRESSION,
    NodeType.TERNARY,
    NodeType.WITH,
    NodeType.TRY,
    NodeType.EXCEPT,
    NodeType.FINALLY,
    NodeType.CONSTANT,
    NodeType.METHOD,
    NodeType.PROPERTY,
    NodeType.DECORATOR,
    NodeType.RETURN,
    NodeType.BREAK,
    NodeType.CONTINUE,
    NodeType.RAISE,
    NodeType.ASSERT
}