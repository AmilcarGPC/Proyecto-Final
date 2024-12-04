"""
Nombre del módulo: contador_fisico.py
Ruta: contador_lineas/core/contadores/contador_fisico.py
Descripción: Cuenta líneas físicas de código Python excluyendo comentarios
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - core.arbol.nodo.Nodo
    - config.node_types.COMMENT_NODE_TYPES, VALID_CODE_NODE_TYPES
    - models.nodos.TipoNodo

Uso:
    from from contador_lineas.core.contadores.contador_fisico import (
        ContadorLineasFisicas
    )
    
    contador = ContadorLineasFisicas()
    total = contador.contar_lineas_fisicas(nodo_raiz)

Notas:
    - Ignora comentarios y docstrings
    - Cuenta imports múltiples como líneas separadas
"""

from contador_lineas.core.arbol.nodo import Nodo
from contador_lineas.config.node_types import (
    COMMENT_NODE_TYPES, VALID_CODE_NODE_TYPES
)
from contador_lineas.models.nodos import TipoNodo


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
        if nodo.tipo == TipoNodo.IMPORT:
            contador += ContadorLineasFisicas._procesar_importacion(nodo)
        elif nodo.tipo == TipoNodo.ASSIGNMENT:
            contador += ContadorLineasFisicas._procesar_asignacion(nodo)
        elif nodo.tipo in COMMENT_NODE_TYPES:
            contador += 0 # Explícitamente ignoramos comentarios
        elif nodo.tipo in VALID_CODE_NODE_TYPES:
            contador += 1

        # Procesamiento recursivo necesario para mantener la estructura
        # jerárquica del árbol
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
        # Los imports con 'from' siempre cuentan como una línea sin importar
        # los elementos que importe, esto de acuerdo al estándar de codificación
        if not "," in nodo.contenido or nodo.contenido.startswith("from"):
            return 1

        # Cada elemento en un import múltiple cuenta como una línea física
        # separada, según el estándar de codificación
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
        # Solo procesamos como múltiples líneas si hay múltiples variables
        # siendo asignadas (lado izquierdo del =)
        if not "," in nodo.contenido.split("=")[0]:
            return 1

        # Cada variable en una asignación múltiple cuenta como una línea física
        # separada, de acuerdo con el estándar de codificación
        elementos = nodo.contenido.split("=")[0].split(",")
        return len([elemento.strip() for elemento in elementos])
