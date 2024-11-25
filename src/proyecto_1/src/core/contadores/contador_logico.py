"""
Nombre del módulo: contador_logico.py
Ruta: src/core/contadores/contador_logico.py
Descripción: Cuenta líneas lógicas de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18/11/2024
Última Actualización: 18/11/2024

Dependencias:
    - core.arbol.nodo.Nodo
    - config.node_types.LOGICAL_NODE_TYPES

Uso:
    from core.contadores.contador_logico import ContadorLineasLogicas
    
    contador = ContadorLineasLogicas()
    total = contador.contar_lineas_logicas(nodo_raiz)

Notas:
    - Cuenta declaraciones ejecutables como líneas lógicas
    - Ignora comentarios y docstrings
"""
from core.arbol.nodo import Nodo
from config.node_types import LOGICAL_NODE_TYPES


class ContadorLineasLogicas:
    """
    Cuenta líneas lógicas de código Python.

    Procesa un árbol sintáctico para contar declaraciones ejecutables,
    excluyendo comentarios y docstrings.

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
        contador = 0
            
        if nodo.tipo in LOGICAL_NODE_TYPES:
            contador += 1
            
        for hijo in nodo.hijos:
            contador += ContadorLineasLogicas._contar_lineas_nodo(hijo)
                
        return contador