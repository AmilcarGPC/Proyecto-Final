"""
Nombre del módulo: arbol_sintactico.py
Ruta: contador_lineas/core/arbol/arbol_sintactico.py
Descripción: Define la estructura del árbol sintáctico para archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - utils.constructor_arbol.ConstructorArbol
    - utils.impresion_arbol.imprimir_arbol

Uso:
    from contador_lineas.core.arbol.arbol_sintactico import ArbolArchivoPython
    arbol = ArbolArchivoPython(contenido_archivo)
    arbol.imprimir_arbol()

Notas:
    - Implementa representación jerárquica del código fuente
"""

from contador_lineas.core.arbol.constructor_arbol import ConstructorArbol
from contador_lineas.utils.impresion_arbol import imprimir_arbol


class ArbolArchivoPython:
    """
    Representa un árbol sintáctico de un archivo Python.

    Attributes:
        constructor (ConstructorArbol): Constructor del árbol sintáctico
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
        # Usamos ConstructorArbol para construir el árbol sintáctico ya que la
        # construcción requiere un análisis complejo del código que se mantiene
        # separado de la representación del árbol
        self.constructor = ConstructorArbol()
        self.raiz = self.constructor.construir(file_content)

    def imprimir_arbol(self) -> None:
        """
        Imprime la estructura del árbol en consola.
        """
        imprimir_arbol(self.raiz)
