"""
Nombre del módulo: conftest.py
Ruta: contador_lineas/tests/conftest.py
Descripción: Define configuración global para pruebas unitarias y de integración
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - pytest
    - contador_lineas.core.arbol.arbol_sintactico.ArbolArchivoPython

Uso:
    from contador_lineas.tests.conftest import crear_arbol_desde_string

Notas:
    - Define fixtures para pruebas unitarias y de integración
    - Proporciona funciones de ayuda para crear árboles sintácticos desde strings
"""

from contador_lineas.core.arbol.arbol_sintactico import ArbolArchivoPython

def crear_arbol_desde_string(codigo: str) -> ArbolArchivoPython:
    """
    Crea un árbol sintáctico a partir de un string válido de código Python.

    Args:
        codigo (str): Código Python en formato de string

    Returns:
        ArbolArchivoPython: Árbol sintáctico generado a partir del código

    Example:
        >>> arbol = crear_arbol_desde_string("x = 1\ny = 2")
        >>> arbol.raiz
    """
    lineas = codigo.strip().split('\n')
    return ArbolArchivoPython(lineas)