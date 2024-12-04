"""
Nombre del módulo: arbol_sintactico.py
Ruta: analizador_cambios/core/arbol/arbol_sintactico.py
Descripción: Define la estructura del árbol sintáctico para archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 28-11-2024
Última Actualización: 02-12-2024

Dependencias:
    - utils.constructor_arbol.ConstructorArbol
    - utils.impresion_arbol.imprimir_arbol

Uso:
    from analizador_cambios.core.arbol.arbol_sintactico import (
        ArbolArchivoPython
    )
    arbol = ArbolArchivoPython(contenido_archivo)
    arbol.imprimir_arbol()

Notas:
    - Implementa representación jerárquica del código fuente
"""

from typing import List

from analizador_cambios.core.arbol.nodo import Nodo
from analizador_cambios.core.arbol.constructor_arbol import ConstructorArbol
from contador_lineas.models.nodos import TipoNodo
from contador_lineas.utils.impresion_arbol import imprimir_arbol


class ArbolArchivoPython:
    """
    Representa un árbol sintáctico de un archivo Python.

    Attributes:
        constructor (ConstructorArbol): Constructor del árbol sintáctico
        raiz (Nodo): Nodo raíz del árbol sintáctico
        mapeo_lineas (Dict[int, Nodo]): Mapeo de número de nodo a lineas

    Methods:
        imprimir_arbol() -> None:
            Imprime el árbol sintáctico en consola.

    Example:
        >>> contenido = ["def suma(a, b):", "    return a + b"]
        >>> arbol = ArbolArchivoPython(contenido)
        >>> arbol.imprimir_arbol()
    """

    def __init__(self, file_content: List[str]):
        self.constructor = ConstructorArbol()
        self.raiz = self.constructor.construir(file_content)
        self.mapeo_lineas = self.constructor.arbol_a_lineas

    def imprimir_arbol(self) -> None:
        """
        Imprime la estructura del árbol en consola.
        """
        imprimir_arbol(self.raiz)

    def obtener_nodos_clase(self) -> List[Nodo]:
        """
        Obtiene los nodos de las clases presentes en el archivo.

        Returns:
            List[str]: Lista con los nombres de las clases
        """
        if not self.raiz:
            return []

        clases = []
        for nodo in self.raiz.hijos:
            if nodo.tipo == TipoNodo.CLASS:
                clases.append(nodo)
        return clases

    def obtener_nodos_metodos(self, clase: Nodo) -> List[Nodo]:
        """
        Obtiene los nodos de los métodos presentes en el archivo.

        Args:
            clase (Nodo): Nodo de la clase a analizar

        Returns:
            List[str]: Lista con los nombres de los métodos
        """
        if not self.raiz and clase.tipo != TipoNodo.CLASS:
            return []

        metodos = []
        for nodo in clase.hijos:
            if nodo.tipo == TipoNodo.METHOD:
                metodos.append(nodo)
        return metodos

    def obtener_nodo_otros(self) -> Nodo:
        """
        Crea un nodo que agrupa todos los elementos que no son clases.

        Returns:
            Nodo: Nodo tipo clase con nombre "otros" que contiene
                    todos los elementos que no son clases
        """
        if not self.raiz:
            return Nodo("otros", TipoNodo.CLASS, 0)

        # Filtrar nodos que no son clases y ajustar indentación
        nodos_no_clase = [
            nodo for nodo in self.raiz.hijos
            if nodo.tipo != TipoNodo.CLASS
        ]

        # Incrementar indentación de cada nodo en 4
        for nodo in nodos_no_clase:
            nodo.nivel_indentacion += 4

        # Crear nodo otros
        nodo_otros = Nodo(TipoNodo.CLASS, "", 0)
        nodo_otros.hijos = nodos_no_clase

        return nodo_otros
