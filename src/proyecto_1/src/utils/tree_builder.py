"""
Module name: tree_builder.py
Route: src/utils/tree_builder.py
Description: Build the syntax tree from the file content.
Project: LOC Counter System
Author: Amílcar Pérez
Organization: Equipo 3
License: MIT
Date Created: 17-11-2024
Last Update: 18-11-2024

Dependencies:
    - typing.List
    - models.nodes.Node
    - models.nodes.NodeType
    - utils.node_analyzer.NodeTypeAnalyzer
    - config.node_types.PARENT_NODE_TYPES

Usage:
    from utils.tree_builder import TreeBuilder
    builder = TreeBuilder()

Notes:
    - Tree must be built using the TreeBuilder class.
"""
from typing import List

from core.arbol.nodo import Nodo
from models.nodes import NodeType
from utils.node_analyzer import NodeTypeAnalyzer
from utils.line_formatter import LineFormatter
from config.node_types import PARENT_NODE_TYPES
from core.analizadores.analizador_cadenas import AnalizadorCadenas

class TreeBuilder:
    def __init__(self, multilines_worth_1: bool = True):
        self.multilines_worth_1 = multilines_worth_1
        self.type_analyzer = NodeTypeAnalyzer()
        self.multiline_buffer = []
        self.open_delimiters = 0
        self.in_multiline_string = False
        self.string_delimiter = None

    def _is_string_assignment(self, line: str) -> bool:
        """Check if line contains a string assignment."""
        # Remove spaces and check if it's an assignment with triple quotes
        stripped = line.strip()
        return ('=' in stripped and 
                ('"""' in stripped.split('=')[1] or 
                "'''" in stripped.split('=')[1]))

    def _is_valid_docstring_start(self, line: str) -> bool:
        """Check if line starts a valid docstring."""
        stripped = line.strip()
        return (stripped.startswith('"""') or 
                stripped.startswith("'''"))

    def _analyze_docstring(self, line: str) -> bool:
        """
        Analyzes if line is complete based on docstring rules.
        Returns True if line is complete, False if part of multiline docstring.
        """
        stripped = line.strip()
        # Handle string assignments differently
        if self._is_string_assignment(stripped):
            if not self.in_multiline_string:
                pos1 = AnalizadorCadenas.encontrar_sin_comillas(stripped, '"""', 0)
                pos2 = AnalizadorCadenas.encontrar_sin_comillas(stripped, "'''", 0)

                if pos1 == -1 and pos2 == -1:
                    return not self.in_multiline_string
                
                quote_count = stripped.count('"""') + stripped.count("'''")
                if quote_count == 2:
                    return True
                self.in_multiline_string = True
                self.string_delimiter = '"""' if '"""' in stripped else "'''"
                return False
    
        
        # Handle actual docstrings
        elif '"""' in stripped or "'''" in stripped:
            pos1 = AnalizadorCadenas.encontrar_sin_comillas(stripped, '"""', 0)
            pos2 = AnalizadorCadenas.encontrar_sin_comillas(stripped, "'''", 0)

            if pos1 == -1 and pos2 == -1:
                return not self.in_multiline_string

            if not self.in_multiline_string and self._is_valid_docstring_start(stripped):
                self.in_multiline_string = True
                self.string_delimiter = '"""' if '"""' in stripped else "'''"
                return False
            elif self.in_multiline_string and self.string_delimiter in stripped:
                self.in_multiline_string = False
                self.string_delimiter = None
                return True
            return False
                
        return not self.in_multiline_string

    def _analyze_delimiters(self, line: str) -> bool:
        """
        Analyzes if line is complete based on delimiter count rules.
        Returns True if line is complete, False if incomplete.
        """
        pos1 = AnalizadorCadenas.encontrar_sin_comillas(line, '(', 0)
        pos2 = AnalizadorCadenas.encontrar_sin_comillas(line, ")", 0)
        pos3 = AnalizadorCadenas.encontrar_sin_comillas(line, '[', 0)   
        pos4 = AnalizadorCadenas.encontrar_sin_comillas(line, "]", 0)
        pos5 = AnalizadorCadenas.encontrar_sin_comillas(line, '{', 0)
        pos6 = AnalizadorCadenas.encontrar_sin_comillas(line, "}", 0)

        if pos1 == -1 and pos2 == -1 and pos3 == -1 and pos4 == -1 and pos5 == -1 and pos6 == -1:
            return self.open_delimiters == 0 and not line.rstrip().endswith('\\')
        
        if self.multilines_worth_1:
            self.open_delimiters += (AnalizadorCadenas.contar_sin_comillas(line, '(') + 
                     AnalizadorCadenas.contar_sin_comillas(line, '[') + 
                     AnalizadorCadenas.contar_sin_comillas(line, '{'))
            self.open_delimiters -= (AnalizadorCadenas.contar_sin_comillas(line, ')') + 
                      AnalizadorCadenas.contar_sin_comillas(line, ']') + 
                      AnalizadorCadenas.contar_sin_comillas(line, '}'))
              
        return self.open_delimiters == 0 and not line.rstrip().endswith('\\')

    def _is_line_complete(self, line: str) -> bool:
        """
        Determines if a line is complete by checking both docstrings and delimiters.
        """
        docstring_complete = self._analyze_docstring(line)
        if not docstring_complete:
            return False
          
        return self._analyze_delimiters(line)
    
    def build(self, lines: List[str]) -> Nodo:
        raiz = Nodo(NodeType.ROOT, "raiz", -1)
        current_parent = raiz
        indent_stack = [(raiz, -1)]
        i = 0
        j = 0
        while i < len(lines):
            line = lines[i]
            
            if not line.strip():
                i += 1
                continue

            
            # Format long lines
            formatted_lines = LineFormatter.format_line(line)
            if len(formatted_lines) > 1:
                self.multiline_buffer = [l.strip() for l in formatted_lines]
            j = i
            if not self._is_line_complete(line.strip()):
                
                self.multiline_buffer = [line.strip()[:-1] if line.strip().endswith('\\') else line.strip()]
                while i + 1 < len(lines) and not self._is_line_complete(lines[i + 1].strip()):
                    i += 1
                    self.multiline_buffer.append(lines[i].strip()[:-1] if lines[i].strip().endswith('\\') else lines[i].strip())

                if i + 1 < len(lines):
                    i += 1
                    self.multiline_buffer.append(lines[i].strip())
                # Join multiline statement
                line = ' '.join(self.multiline_buffer)
                self.multiline_buffer = []
                self.open_delimiters = 0
            indent = len(lines[j]) - len(lines[j].lstrip())
            node_type = self.type_analyzer.get_node_type(line)
            new_node = Nodo(node_type, line.strip(), indent)

            while indent_stack and indent <= indent_stack[-1][1]:
                indent_stack.pop()
                if indent_stack:
                    current_parent = indent_stack[-1][0]

            current_parent.agregar_hijo(new_node)
            
            if self._can_have_children(node_type):
                current_parent = new_node
                indent_stack.append((new_node, indent))
                
            i += 1

        return raiz

    def _can_have_children(self, node_type: NodeType) -> bool:
        return node_type in PARENT_NODE_TYPES