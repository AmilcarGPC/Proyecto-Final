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

from analizador_cambios.utils.tree_builder import TreeBuilder # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.86%
from analizador_cambios.utils.impresion_arbol import imprimir_arbol # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.87%
from analizador_cambios.core.arbol.nodo import Nodo # AGREGADA TOTALMENTE NUEVA
from analizador_cambios.models.nodos import TipoNodo # AGREGADA TOTALMENTE NUEVA


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
        self.mapeo_lineas = self.constructor.tree_2_lines # AGREGADA TOTALMENTE NUEVA

    def imprimir_arbol(self) -> None:
        """
        Imprime la estructura del árbol en consola.
        """
        imprimir_arbol(self.raiz)

    def obtener_nodos_clase(self) -> list[Nodo]: # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        Obtiene los nodos de las clases presentes en el archivo. # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Returns: # AGREGADA TOTALMENTE NUEVA
            list[str]: Lista con los nombres de las clases # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        if not self.raiz: # AGREGADA TOTALMENTE NUEVA
            return [] # AGREGADA TOTALMENTE NUEVA
        
        clases = [] # AGREGADA TOTALMENTE NUEVA
        for nodo in self.raiz.hijos: # AGREGADA TOTALMENTE NUEVA
            if nodo.tipo == TipoNodo.CLASS: # AGREGADA TOTALMENTE NUEVA
                clases.append(nodo) # AGREGADA TOTALMENTE NUEVA
        return clases # AGREGADA TOTALMENTE NUEVA
    
    def obtener_nodos_metodos(self, clase: Nodo) -> list[Nodo]: # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        Obtiene los nodos de los métodos presentes en el archivo. # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Args: # AGREGADA TOTALMENTE NUEVA
            clase (Nodo): Nodo de la clase a analizar # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Returns: # AGREGADA TOTALMENTE NUEVA
            list[str]: Lista con los nombres de los métodos # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        if not self.raiz and clase.tipo != TipoNodo.CLASS: # AGREGADA TOTALMENTE NUEVA
            return [] # AGREGADA TOTALMENTE NUEVA
        
        metodos = [] # AGREGADA TOTALMENTE NUEVA
        for nodo in clase.hijos: # AGREGADA TOTALMENTE NUEVA
            if nodo.tipo == TipoNodo.METHOD: # AGREGADA TOTALMENTE NUEVA
                metodos.append(nodo) # AGREGADA TOTALMENTE NUEVA
        return metodos # AGREGADA TOTALMENTE NUEVA
    
    def obtener_nodo_otros(self) -> Nodo: # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        Crea un nodo que agrupa todos los elementos que no son clases. # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Returns: # AGREGADA TOTALMENTE NUEVA
            Nodo: Nodo tipo clase con nombre "otros" que contiene # AGREGADA TOTALMENTE NUEVA
                    todos los elementos que no son clases # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        if not self.raiz: # AGREGADA TOTALMENTE NUEVA
            return Nodo("otros", TipoNodo.CLASS, 0) # AGREGADA TOTALMENTE NUEVA
        
        # Filtrar nodos que no son clases y ajustar indentación # AGREGADA TOTALMENTE NUEVA
        nodos_no_clase = [
            nodo for nodo in self.raiz.hijos 
            if nodo.tipo != TipoNodo.CLASS
        ] # AGREGADA TOTALMENTE NUEVA (las 4 líneas previas cuentan como 1)
        
        # Incrementar indentación de cada nodo en 4 # AGREGADA TOTALMENTE NUEVA
        for nodo in nodos_no_clase: # AGREGADA TOTALMENTE NUEVA
            nodo.nivel_indentacion += 4 # AGREGADA TOTALMENTE NUEVA
        
        # Crear nodo otros # AGREGADA TOTALMENTE NUEVA
        nodo_otros = Nodo(TipoNodo.CLASS, "", 0) # AGREGADA TOTALMENTE NUEVA
        nodo_otros.hijos = nodos_no_clase # AGREGADA TOTALMENTE NUEVA
        
        return nodo_otros # AGREGADA TOTALMENTE NUEVA
