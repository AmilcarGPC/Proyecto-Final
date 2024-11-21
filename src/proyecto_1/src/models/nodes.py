from enum import Enum
from typing import List, Optional

class NodeType(Enum):
    ROOT = "root"
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

class Node:
    def __init__(self, type: NodeType, content: str, indent_level: int):
        self.type = type
        self.content = content
        self.indent_level = indent_level
        self.children: List[Node] = []
        self.parent: Optional[Node] = None

    def add_child(self, child: 'Node'):
        child.parent = self
        self.children.append(child)