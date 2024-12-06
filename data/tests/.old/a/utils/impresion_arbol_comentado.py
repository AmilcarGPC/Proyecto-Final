"""
Nombre del módulo: impresion_arbol.py
Ruta: src/utils/impresion_arbol.py
Descripción: Imprime la estructura de árbol de un archivo Python representado \
como árbol sintáctico.
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 17-11-2024
Última Actualización: 17-11-2024

Dependencias:
    - models.nodos.Nodo

Uso:
    from utils.impresion_arbol import imprimir_arbol

    imprimir_arbol(raiz)

Notas:
    - El árbol debe ser construido usando la clase TreeBuilder
"""

from contador_lineas.core.arbol.nodo import Nodo # BORRADA


def imprimir_arbol(raiz: Nodo) -> None:
    """
    Imprime la estructura completa del árbol.

    Args:
        raiz (Nodo): Nodo raíz del árbol a imprimir

    Example:
        >>> imprimir_arbol(raiz)
        Árbol del Archivo Python:
        └── [function] def main():
    """
    print("Árbol del Archivo Python:")
    for i, hijo in enumerate(raiz.hijos):
        es_ultimo = i == len(raiz.hijos) - 1
        _imprimir_nodo(hijo, "", es_ultimo)

        
def _imprimir_nodo(
    nodo: Nodo, 
    prefijo: str = "", 
    es_ultimo: bool = True
) -> None:
    """
    Imprime un nodo individual del árbol con su formato.

    Args:
        nodo (Nodo): Nodo a imprimir
        prefijo (str): Caracteres de indentación. Por defecto ""
        es_ultimo (bool): Si es el último hijo. Por defecto True

    Example:
        >>> _imprimir_nodo(nodo, "", True)
        └── [assignment] x = 1
    """
    conector = "└── " if es_ultimo else "├── "
    print(f"{prefijo}{conector}[{nodo.tipo.value}] {nodo.contenido}")
    
    prefijo_hijo = prefijo + ("    " if es_ultimo else "│   ")
    
    for i, hijo in enumerate(nodo.hijos):
        es_ultimo_hijo = i == len(nodo.hijos) - 1
        _imprimir_nodo(hijo, prefijo_hijo, es_ultimo_hijo)
