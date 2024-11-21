from models.nodes import NodeType
from typing import Optional

class NodeTypeAnalyzer:
    def __init__(self):
        self._in_docstring = False
        self._in_class = False
        self._is_module_level = True
        self._in_method = False
        self._current_class = None

    def _check_docstring(self, line: str) -> Optional[NodeType]:
        if self._in_docstring:
            if line.endswith('"""') or line.endswith("'''"):
                self._in_docstring = False
                return self._get_docstring_type()
            return NodeType.COMMENT
        
        if line.startswith('"""') or line.startswith("'''"):
            self._in_docstring = True
            return self._get_docstring_type()
        return None

    def _get_docstring_type(self) -> NodeType:
        if self._is_module_level:
            return NodeType.MODULE_DOCSTRING
        elif self._in_class:
            return NodeType.CLASS_DOCSTRING
        return NodeType.FUNCTION_DOCSTRING

    def _check_definitions(self, line: str) -> Optional[NodeType]:
        if line.startswith('def '):
            self._is_module_level = False
            if self._in_class:
                self._in_method = True
                return NodeType.METHOD
            return NodeType.FUNCTION
        if line.startswith('class '):
            self._in_class = True
            self._in_method = False
            self._current_class = line
            return NodeType.CLASS
        return None

    def _check_conditional_statements(self, line: str) -> Optional[NodeType]:
        control_flow_map = {
            'if ': NodeType.IF,
            'elif ': NodeType.ELIF,
            'else:': NodeType.ELSE,
            'for ': NodeType.FOR,
            'while ': NodeType.WHILE,
            'match ': NodeType.MATCH,
            'case ': NodeType.CASE,
        }
        for start, node_type in control_flow_map.items():
            if line.startswith(start):
                return node_type
        return None
    
    def _check_special_operations(self, line: str) -> Optional[NodeType]:
        if line.startswith('with '):
            return NodeType.WITH
        if line.startswith('try:'):
            return NodeType.TRY
        if line.startswith('except'):
            return NodeType.EXCEPT
        if line.startswith('finally:'):
            return NodeType.FINALLY
        if ' if ' in line and ' else ' in line and not line.startswith('if '):
            return NodeType.TERNARY
        return None
    
    def _check_comprehensions(self, line: str) -> Optional[NodeType]:
        if '[' in line and ']' in line and 'for' in line:
            return NodeType.LIST_COMPREHENSION
        if '{' in line and '}' in line and ':' in line and 'for' in line:
            return NodeType.DICT_COMPREHENSION
        if '{' in line and '}' in line and 'for' in line:
            return NodeType.SET_COMPREHENSION
        if '(' in line and ')' in line and 'for' in line:
            return NodeType.GENERATOR_EXPRESSION
        return None

    def _check_jump_statements(self, line: str) -> Optional[NodeType]:
        if line.startswith('return '):
            return NodeType.RETURN
        if line.startswith('break'):
            return NodeType.BREAK
        if line.startswith('continue'):
            return NodeType.CONTINUE
        if line.startswith('raise '):
            return NodeType.RAISE
        if line.startswith('assert '):
            return NodeType.ASSERT
        return None
    
    def _check_decorators_and_properties(self, line: str) -> Optional[NodeType]:
        if line.startswith('@'):
            return NodeType.DECORATOR
        if '@property' in line:
            return NodeType.PROPERTY
        return None

    def _check_constants_and_imports(self, line: str) -> Optional[NodeType]:
        if line.isupper() and '=' in line:
            return NodeType.CONSTANT
        if line.startswith('import ') or line.startswith('from '):
            return NodeType.IMPORT
        return None

    def get_node_type(self, line: str) -> NodeType:
        line = line.strip()
        
        # Existing checks
        docstring_type = self._check_docstring(line)
        if docstring_type:
            return docstring_type

        if line.startswith('#'):
            return NodeType.COMMENT
        
        decorator_import_type = self._check_decorators_and_properties(line)
        if decorator_import_type:
            return decorator_import_type
        
        const_prop_type = self._check_constants_and_imports(line)
        if const_prop_type:
            return const_prop_type

        definition_type = self._check_definitions(line)
        if definition_type:
            return definition_type

        control_flow_type = self._check_conditional_statements(line)
        if control_flow_type:
            return control_flow_type

        # New checks
        comprehension_type = self._check_comprehensions(line)
        if comprehension_type:
            return comprehension_type

        special_op_type = self._check_special_operations(line)
        if special_op_type:
            return special_op_type

        flow_control_type = self._check_jump_statements(line)
        if flow_control_type:
            return flow_control_type

        # Default cases
        if '=' in line:
            return NodeType.ASSIGNMENT
        return NodeType.EXPRESSION