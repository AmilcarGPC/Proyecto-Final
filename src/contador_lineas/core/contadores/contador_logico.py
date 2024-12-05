"""
Nombre del módulo: contador_logico.py
Ruta: contador_lineas/core/contadores/contador_logico.py
Descripción: Cuenta líneas lógicas de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - core.arbol.nodo.Nodo
    - config.node_types.LOGICAL_NODE_TYPES

Uso:
    from contador_lineas.core.contadores.contador_logico import (
        ContadorLineasLogicas
    )
    
    contador = ContadorLineasLogicas()
    total = contador.contar_lineas_logicas(nodo_raiz)

Notas:
    - Cuenta declaraciones ejecutables como líneas lógicas
    - Ignora comentarios y docstrings
"""

from contador_lineas.core.arbol.nodo import Nodo
from contador_lineas.config.node_types import LOGICAL_NODE_TYPES
from contador_lineas.models.nodos import TipoNodo

class ContadorLineasLogicas:
    """
    Cuenta líneas lógicas de código Python.

    Procesa un árbol sintáctico para contar declaraciones ejecutables,
    excluyendo cualquier línea que no sea una estructura lógica.

    Methods:
        contar_lineas_logicas(raiz: Nodo) -> int:
            Cuenta el total de líneas lógicas en el árbol.

    Example:
        >>> contador = ContadorLineasLogicas()
        >>> total = contador.contar_lineas_logicas(nodo_raiz)
    """

    @staticmethod
    def contar_lineas_logicas(raiz: Nodo) -> int:
        """
        Cuenta líneas lógicas totales en un árbol sintáctico.

        Args:
            raiz (Nodo): Nodo raíz del árbol sintáctico

        Returns:
            int: Total de líneas lógicas encontradas

        Example:
            >>> contar_lineas_logicas(nodo_raiz)
            7
        """
        return ContadorLineasLogicas._contar_lineas_nodo(raiz)

    @staticmethod
    def _contar_lineas_nodo(nodo: Nodo) -> int:
        """
        Cuenta líneas lógicas para un nodo específico.

        Args:
            nodo (Nodo): Nodo a procesar

        Returns:
            int: Líneas lógicas en este nodo

        Example:
            >>> _contar_lineas_nodo(nodo)
            1
        """
        if nodo.tipo != TipoNodo.ROOT and len(nodo.contenido) == 0:
            return 0
        
        contador = 0

        # Solo contamos nodos que representan declaraciones ejecutables
        # (definidos en LOGICAL_NODE_TYPES) ignorando cualquier otro tipo de
        # elemento
        if nodo.tipo in LOGICAL_NODE_TYPES:
            contador += 1

        # El recorrido recursivo es necesario ya que las declaraciones lógicas
        # pueden estar anidadas (por ejemplo, dentro de funciones o clases)
        for hijo in nodo.hijos:
            contador += ContadorLineasLogicas._contar_lineas_nodo(hijo)

        return contador
