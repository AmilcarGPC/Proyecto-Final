"""
Nombre del módulo: contador_fisico.py
Ruta: src/core/contadores/contador_fisico.py
Descripción: Cuenta líneas físicas de código Python excluyendo comentarios
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - typing.List
    - core.arbol.nodo.Nodo
    - config.node_types.COMMENT_NODE_TYPES, VALID_CODE_NODE_TYPES
    - models.nodos.TipoNodo

Uso:
    from core.contadores.contador_fisico import ContadorLineasFisicas
    
    contador = ContadorLineasFisicas()
    total = contador.contar_lineas_fisicas(nodo_raiz)

Notas:
    - Ignora comentarios y docstrings
    - Cuenta imports múltiples como líneas separadas
"""

from typing import List

from analizador_cambios.core.arbol.nodo import Nodo
from analizador_cambios.config.node_types import COMMENT_NODE_TYPES, VALID_CODE_NODE_TYPES
from analizador_cambios.models.nodos import TipoNodo


class ContadorLineasFisicas:
    """
    Cuenta líneas físicas de código Python.

    Procesa un árbol sintáctico para contar líneas físicas,
    excluyendo comentarios y manejando casos especiales.

    Methods:
        contar_lineas_fisicas(raiz: Nodo) -> int:
            Cuenta el total de líneas físicas en el árbol.

    Example:
        >>> contador = ContadorLineasFisicas()
        >>> total = contador.contar_lineas_fisicas(nodo_raiz)
    """
    
    @staticmethod
    def contar_lineas_fisicas(raiz: Nodo) -> int:
        """
        Cuenta líneas físicas totales en un árbol sintáctico.

        Args:
            raiz (Nodo): Nodo raíz del árbol sintáctico

        Returns:
            int: Total de líneas físicas encontradas

        Example:
            >>> contar_lineas_fisicas(nodo_raiz)
            20
        """
        return ContadorLineasFisicas._contar_lineas_nodo(raiz)
    
    @staticmethod
    def _contar_lineas_nodo(nodo: Nodo) -> int:
        """
        Cuenta líneas físicas para un nodo específico.

        Args:
            nodo (Nodo): Nodo a procesar

        Returns:
            int: Líneas físicas en este nodo

        Example:
            >>> _contar_lineas_nodo(nodo)
            4
        """
        contador = 0
        #old = contador
        if nodo.tipo == TipoNodo.IMPORT:
            contador += ContadorLineasFisicas._procesar_importacion(nodo)
        elif nodo.tipo == TipoNodo.ASSIGNMENT:
            contador += ContadorLineasFisicas._procesar_asignacion(nodo)
        elif nodo.tipo in COMMENT_NODE_TYPES:
            contador += 0
        elif nodo.tipo in VALID_CODE_NODE_TYPES:
            contador += 1
        
        #print(f"contenido: {nodo.contenido} - vale: {contador - old}")
            
        for hijo in nodo.hijos:
            contador += ContadorLineasFisicas._contar_lineas_nodo(hijo)
                
        return contador
    
    @staticmethod
    def _procesar_importacion(nodo: Nodo) -> int:
        """
        Cuenta líneas físicas para un nodo de importación.

        Args:
            nodo (Nodo): Nodo de importación a procesar

        Returns:
            int: Número de líneas físicas equivalentes

        Example:
            >>> _procesar_importacion(nodo_import)
            2  # Para 'import os, sys'
        """
        if not "," in nodo.contenido or nodo.contenido.startswith("from"):
            return 1
            
        elementos = nodo.contenido.split("import")[1].split(",")
        return len([elemento.strip() for elemento in elementos])
    
    @staticmethod
    def _procesar_asignacion(nodo: Nodo) -> int:
        """
        Cuenta líneas físicas para un nodo de asignación.

        Args:
            nodo (Nodo): Nodo de asignación a procesar

        Returns:
            int: Número de líneas físicas equivalentes

        Example:
            >>> _procesar_asignacion(nodo_asignacion)
            2  # Para 'x, y = 1, 2'
        """
        if not "," in nodo.contenido.split("=")[0]:
            return 1
            
        elementos = nodo.contenido.split("=")[0].split(",")
        return len([elemento.strip() for elemento in elementos])
