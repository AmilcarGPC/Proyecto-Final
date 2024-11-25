"""
Module name: tree_printer.py
Route: src/utils/tree_printer.py
Description: Print the tree structure of a Python file represented as a syntax tree.
Project: LOC Counter System
Author: Amílcar Pérez
Organization: Equipo 3
License: MIT
Date Created: 17-11-2024
Last Update: 17-11-2024

Dependencies:
    - models.nodes.Node

Usage:
    from utils.tree_printer import TreePrinter
    TreePrinter.imprimir_arbol(raiz)

Notes:
    - Tree must be built using the TreeBuilder class.
"""

from core.arbol.nodo import Nodo

class TreePrinter:
    @staticmethod
    def imprimir_arbol(raiz: Nodo):
        def _print_node(nodo: Nodo, prefix: str = "", is_last: bool = True):
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}[{nodo.tipo.value}] {nodo.contenido}")
            
            child_prefix = prefix + ("    " if is_last else "│   ")
            
            for i, hijo in enumerate(nodo.hijos):
                is_last_child = i == len(nodo.hijos) - 1
                _print_node(hijo, child_prefix, is_last_child)

        print("Python File Tree:")
        for i, hijo in enumerate(raiz.hijos):
            is_last = i == len(raiz.hijos) - 1
            _print_node(hijo, "", is_last)