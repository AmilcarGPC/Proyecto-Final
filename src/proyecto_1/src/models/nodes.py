# src/models/nodes.py
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

class NodeType(Enum):
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
class ExpressionInfo:
    type: NodeType
    nested_expressions: List['ExpressionInfo']
    start_pos: int
    end_pos: int  
    expression: str