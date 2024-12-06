"""
Nombre del módulo: nodos.py
Ruta: src/models/nodos.py
Descripción: Define los tipos de nodos y su estructura para el análisis sintáctico
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - dataclasses
    - enum
    - typing

Uso:
    from models.nodos import TipoNodo, InformacionExpresion

    nodo = InformacionExpresion(TipoNodo.ROOT, [], 0, 10, "código")

Notas:
    - Los nodos representan diferentes estructuras sintácticas de Python
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class TipoNodo(Enum):
    """
    Define los tipos de nodos posibles en el árbol sintáctico.

    Attributes:
        value (str): Identificador del tipo de nodo

    Example:
        >>> tipo = TipoNodo.ROOT
        >>> tipo.value
        'raiz'
    """

    ROOT = "raiz"
    IMPORT = "import"
    ASSIGNMENT = "assignment"
    FUNCTION = "function"
    CLASS = "class"
    IF = "if"
    ELIF = "elif"
    ELSE = "else"
    FOR = "for"
    WHILE = "while"
    MATCH = "match"
    CASE = "case"
    EXPRESSION = "expression"
    MODULE_DOCSTRING = "module_docstring"
    FUNCTION_DOCSTRING = "function_docstring"
    CLASS_DOCSTRING = "class_docstring"
    COMMENT = "comment"
    INLINE_COMMENT = "inline_comment"
    LIST_COMPREHENSION = "list_comprehension"
    DICT_COMPREHENSION = "dict_comprehension"
    SET_COMPREHENSION = "set_comprehension"
    GENERATOR_EXPRESSION = "generator_expression"
    TERNARY = "ternary_operator"
    WITH = "with_statement"
    TRY = "try"
    EXCEPT = "except"
    FINALLY = "finally"
    CONSTANT = "constant"
    METHOD = "method"
    PROPERTY = "property"
    DECORATOR = "decorator"
    RETURN = "return"
    BREAK = "break"
    CONTINUE = "continue"
    RAISE = "raise"
    ASSERT = "assert"


@dataclass
class InformacionExpresion:
    """
    Almacena información sobre una expresión en el código fuente.

    Attributes:
        tipo (TipoNodo): Tipo de nodo que representa
        expresiones_anidadas (List[InformacionExpresion]): Lista de expresiones contenidas
        posicion_inicial (int): Posición de inicio en el código
        posicion_final (int): Posición final en el código
        expresion (str): Contenido textual de la expresión

    Example:
        >>> nodo = InformacionExpresion(TipoNodo.ROOT, [], 0, 10, "def main():")
    """
    
    tipo: TipoNodo
    expresiones_anidadas: List['InformacionExpresion']
    posicion_inicial: int
    posicion_final: int  
    expresion: str

    def __post_init__(self) -> None:
        """
        Valida que las posiciones sean coherentes.

        Raises:
            ValueError: Si la posición inicial es mayor que la final.
        """
        if self.posicion_inicial > self.posicion_final:
            raise ValueError("La posición inicial debe ser menor que la final")