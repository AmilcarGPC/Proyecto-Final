"""
Nombre del módulo: nodo.py
Ruta: analizador_cambios/core/arbol/nodo.py
Descripción: Define la estructura base de nodos para el árbol sintáctico
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 28-11-2024
Última Actualización: 02-11-2024

Dependencias:
    - typing
    - models.nodos.TipoNodo

Uso:
    from analizador_cambios.core.arbol.nodo import Nodo
    nodo = Nodo(tipo, contenido, nivel_indentacion)

Notas:
    - Implementa estructura jerárquica padre-hijo
"""

from typing import List, Optional

from contador_lineas.models.nodos import TipoNodo


class Nodo:
    """
    Representa un nodo en el árbol sintáctico del analizador.

    Attributes:
        tipo (TipoNodo): Tipo de nodo según la enumeración TipoNodo
        contenido (str): Contenido textual del nodo
        nivel_indentacion (int): Nivel de indentación del nodo
        hijos (List[Nodo]): Lista de nodos hijos
        padre (Optional[Nodo]): Referencia al nodo padre

    Methods:
        agregar_hijo(hijo: Nodo) -> None:
            Agrega un nodo hijo a la lista de hijos.

    Example:
        >>> nodo = Nodo(TipoNodo.FUNCION, "def ejemplo():", 0)
        >>> nodo_hijo = Nodo(TipoNodo.CODIGO, "    return None", 1)
        >>> nodo.agregar_hijo(nodo_hijo)
    """

    def __init__(
            self,
            tipo: TipoNodo,
            contenido: str,
            nivel_indentacion: int,
            numero_nodo = int # Permite el mapeo de un nodo a una línea
        ):
        self.tipo = tipo
        self.contenido = contenido
        self.nivel_indentacion = nivel_indentacion
        self.numero_nodo: int = numero_nodo
        self.hijos: List[Nodo] = []
        self.padre: Optional[Nodo] = None

    def agregar_hijo(self, hijo: 'Nodo') -> None:
        """
        Agrega un nodo hijo al nodo actual.

        Args:
            hijo (Nodo): Nodo a agregar como hijo
        """
        hijo.padre = self
        self.hijos.append(hijo)

    def obtener_nombre_clase(self) -> Optional[str]:
        """
        Obtiene el nombre de la clase si el nodo es de tipo CLASS.
        
        Returns:
            Optional[str]: Nombre de la clase o None si no es nodo clase
        
        Example:
            >>> nodo = Nodo(TipoNodo.CLASS, "class Formateador:", 0)
            >>> print(nodo.obtener_nombre_clase())
            'Formateador'
        """
        if self.tipo != TipoNodo.CLASS:
            return None

        try:
            if len(self.contenido) == 0:
                return ""
            nombre = self.contenido.split("class ")[1].split(":")[0].strip()
            return nombre
        except IndexError:
            return None
