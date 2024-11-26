"""
Nombre del módulo: arbol_sintactico.py
Ruta: src/core/arbol_sintactico.py
Descripción: Define la estructura del árbol sintáctico para archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18/11/2024
Última Actualización: 18/11/2024

Dependencias:
    - utils.tree_builder.TreeBuilder
    - utils.tree_printer.ImpresionArbol

Uso:
    from core.arbol import ArbolArchivoPython
    arbol = ArbolArchivoPython(contenido_archivo)
    arbol.imprimir_arbol()

Notas:
    - Implementa representación jerárquica del código fuente
"""
from utils.tree_builder import TreeBuilder
from utils.tree_printer import ImpresionArbol


class ArbolArchivoPython:
    """
    Representa un árbol sintáctico de un archivo Python.

    Attributes:
        constructor (TreeBuilder): Constructor del árbol sintáctico
        raiz (Nodo): Nodo raíz del árbol sintáctico

    Methods:
        imprimir_arbol() -> None:
            Imprime el árbol sintáctico en consola.

    Example:
        >>> contenido = ["def suma(a, b):", "    return a + b"]
        >>> arbol = ArbolArchivoPython(contenido)
        >>> arbol.imprimir_arbol()
    """
    def __init__(self, file_content: list[str]):
        self.constructor = TreeBuilder()
        self.raiz = self.constructor.build(file_content)

    def imprimir_arbol(self) -> None:
        """
        Imprime la estructura del árbol en consola.
        """
        ImpresionArbol.imprimir_arbol(self.raiz)