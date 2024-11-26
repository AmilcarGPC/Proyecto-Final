from models.nodos import TipoNodo
from typing import Optional

class TipoNodoAnalyzer:
    def __init__(self):
        self._in_docstring = False
        self._in_class = False
        self._is_module_level = True
        self._in_method = False
        self._current_class = None

    def _get_docstring_type(self, line: str) -> TipoNodo:
        if line.startswith('"""') or line.startswith("'''"):
            if self._is_module_level:
                return TipoNodo.MODULE_DOCSTRING
            elif self._in_class:
                return TipoNodo.CLASS_DOCSTRING
            return TipoNodo.FUNCTION_DOCSTRING
        return None

    def _check_definitions(self, line: str) -> Optional[TipoNodo]:
        if line.startswith('def '):
            self._is_module_level = False
            if self._in_class:
                self._in_method = True
                return TipoNodo.METHOD
            return TipoNodo.FUNCTION
        if line.startswith('class '):
            self._in_class = True
            self._in_method = False
            self._current_class = line
            return TipoNodo.CLASS
        return None

    def _check_conditional_statements(self, line: str) -> Optional[TipoNodo]:
        control_flow_map = {
            'if ': TipoNodo.IF,
            'elif ': TipoNodo.ELIF,
            'else:': TipoNodo.ELSE,
            'for ': TipoNodo.FOR,
            'while ': TipoNodo.WHILE,
            'match ': TipoNodo.MATCH,
            'case ': TipoNodo.CASE,
        }
        for start, node_type in control_flow_map.items():
            if line.startswith(start):
                return node_type
        return None
    
    def check_special_operations(self, line: str) -> Optional[TipoNodo]:
        if line.startswith('with '):
            return TipoNodo.WITH
        if line.startswith('try:'):
            return TipoNodo.TRY
        if line.startswith('except'):
            return TipoNodo.EXCEPT
        if line.startswith('finally:'):
            return TipoNodo.FINALLY
        if ' if ' in line and ' else ' in line and not line.startswith('if '):
            return TipoNodo.TERNARY
        return None
    
    def check_comprehensions(self, line: str) -> Optional[TipoNodo]:
        if '[' in line and ']' in line and 'for' in line:
            return TipoNodo.LIST_COMPREHENSION
        if '{' in line and '}' in line and ':' in line and 'for' in line:
            return TipoNodo.DICT_COMPREHENSION
        if '{' in line and '}' in line and 'for' in line:
            return TipoNodo.SET_COMPREHENSION
        if '(' in line and ')' in line and 'for' in line:
            return TipoNodo.GENERATOR_EXPRESSION
        return None

    def _check_jump_statements(self, line: str) -> Optional[TipoNodo]:
        if line.startswith('return '):
            return TipoNodo.RETURN
        if line.startswith('break'):
            return TipoNodo.BREAK
        if line.startswith('continue'):
            return TipoNodo.CONTINUE
        if line.startswith('raise '):
            return TipoNodo.RAISE
        if line.startswith('assert '):
            return TipoNodo.ASSERT
        return None
    
    def _check_decorators_and_properties(self, line: str) -> Optional[TipoNodo]:
        if '@property' in line:
            return TipoNodo.PROPERTY
        if line.startswith('@'):
            return TipoNodo.DECORATOR
        return None

    def _check_constants_and_imports(self, line: str) -> Optional[TipoNodo]:
        if line.isupper() and '=' in line:
            return TipoNodo.CONSTANT
        if line.startswith('import ') or line.startswith('from '):
            return TipoNodo.IMPORT
        return None
    
    def _remove_async_prefix(self, line: str) -> str:
        if line.startswith('async '):
            return line[6:].strip()  # 6 = len('async ')
        return None

    def get_node_type(self, line: str) -> TipoNodo:
        line = line.strip()

        async_prefix = self._remove_async_prefix(line)
        if async_prefix:
            return self.get_node_type(async_prefix)

        docstring_type = self._get_docstring_type(line)
        if docstring_type:
            return docstring_type

        if line.startswith('#'):
            return TipoNodo.COMMENT
        
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
        comprehension_type = self.check_comprehensions(line)
        if comprehension_type:
            return comprehension_type

        special_op_type = self.check_special_operations(line)
        if special_op_type:
            return special_op_type

        flow_control_type = self._check_jump_statements(line)
        if flow_control_type:
            return flow_control_type
        
        decorator_import_type = self._check_decorators_and_properties(line)
        if decorator_import_type:
            return decorator_import_type

        # Default cases
        if '=' in line:
            return TipoNodo.ASSIGNMENT
        return TipoNodo.EXPRESSION