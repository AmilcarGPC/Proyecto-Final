"""
Nombre del módulo: arbol_sintactico.py
Ruta: src/core/arbol_sintactico.py
Descripción: Define la estructura del árbol sintáctico para archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - utils.tree_builder.TreeBuilder
    - utils.impresion_arbol.imprimir_arbol

Uso:
    from core.arbol import ArbolArchivoPython
    arbol = ArbolArchivoPython(contenido_archivo)
    arbol.imprimir_arbol()

Notas:
    - Implementa representación jerárquica del código fuente
"""

from analizador_cambios.utils.tree_builder import TreeBuilder # AÑADIDA EN UN 0.86%
from analizador_cambios.utils.impresion_arbol import imprimir_arbol # AÑADIDA EN UN 0.87%
from analizador_cambios.core.arbol.nodo import Nodo # AÑADIDA EN UN 100%
from analizador_cambios.models.nodos import TipoNodo # AÑADIDA EN UN 100%


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
        self.mapeo_lineas = self.constructor.tree_2_lines # AÑADIDA EN UN 100%

    def imprimir_arbol(self) -> None:
        """
        Imprime la estructura del árbol en consola.
        """
        imprimir_arbol(self.raiz)

    def obtener_nodos_clase(self) -> list[Nodo]: # AÑADIDA EN UN 100%
        """ # AÑADIDA EN UN 100%
        Obtiene los nodos de las clases presentes en el archivo. # AÑADIDA EN UN 100%
 # AÑADIDA EN UN 100%
        Returns: # AÑADIDA EN UN 100%
            list[str]: Lista con los nombres de las clases # AÑADIDA EN UN 100%
        """ # AÑADIDA EN UN 100%
        if not self.raiz: # AÑADIDA EN UN 100%
            return [] # AÑADIDA EN UN 100%
        
        clases = [] # AÑADIDA EN UN 100%
        for nodo in self.raiz.hijos: # AÑADIDA EN UN 100%
            if nodo.tipo == TipoNodo.CLASS: # AÑADIDA EN UN 100%
                clases.append(nodo) # AÑADIDA EN UN 100%
        return clases # AÑADIDA EN UN 100%
    
    def obtener_nodos_metodos(self, clase: Nodo) -> list[Nodo]: # AÑADIDA EN UN 100%
        """ # AÑADIDA EN UN 100%
        Obtiene los nodos de los métodos presentes en el archivo. # AÑADIDA EN UN 100%
 # AÑADIDA EN UN 100%
        Args: # AÑADIDA EN UN 100%
            clase (Nodo): Nodo de la clase a analizar # AÑADIDA EN UN 100%
 # AÑADIDA EN UN 100%
        Returns: # AÑADIDA EN UN 100%
            list[str]: Lista con los nombres de los métodos # AÑADIDA EN UN 100%
        """ # AÑADIDA EN UN 100%
        if not self.raiz and clase.tipo != TipoNodo.CLASS: # AÑADIDA EN UN 100%
            return [] # AÑADIDA EN UN 100%
        
        metodos = [] # AÑADIDA EN UN 100%
        for nodo in clase.hijos: # AÑADIDA EN UN 100%
            if nodo.tipo == TipoNodo.METHOD: # AÑADIDA EN UN 100%
                metodos.append(nodo) # AÑADIDA EN UN 100%
        return metodos # AÑADIDA EN UN 100%
    
    def obtener_nodo_otros(self) -> Nodo: # AÑADIDA EN UN 100%
        """ # AÑADIDA EN UN 100%
        Crea un nodo que agrupa todos los elementos que no son clases. # AÑADIDA EN UN 100%
 # AÑADIDA EN UN 100%
        Returns: # AÑADIDA EN UN 100%
            Nodo: Nodo tipo clase con nombre "otros" que contiene # AÑADIDA EN UN 100%
                    todos los elementos que no son clases # AÑADIDA EN UN 100%
        """ # AÑADIDA EN UN 100%
        if not self.raiz: # AÑADIDA EN UN 100%
            return Nodo("otros", TipoNodo.CLASS, 0) # AÑADIDA EN UN 100%
        
        # Filtrar nodos que no son clases y ajustar indentación # AÑADIDA EN UN 100%
        nodos_no_clase = [
            nodo for nodo in self.raiz.hijos 
            if nodo.tipo != TipoNodo.CLASS
        ] # AÑADIDA EN UN 100% (las 4 líneas previas cuentan como 1)
        
        # Incrementar indentación de cada nodo en 4 # AÑADIDA EN UN 100%
        for nodo in nodos_no_clase: # AÑADIDA EN UN 100%
            nodo.nivel_indentacion += 4 # AÑADIDA EN UN 100%
        
        # Crear nodo otros # AÑADIDA EN UN 100%
        nodo_otros = Nodo(TipoNodo.CLASS, "", 0) # AÑADIDA EN UN 100%
        nodo_otros.hijos = nodos_no_clase # AÑADIDA EN UN 100%
        
        return nodo_otros # AÑADIDA EN UN 100%
