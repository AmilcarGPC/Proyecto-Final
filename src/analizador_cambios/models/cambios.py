"""
Nombre del módulo: cambios.py
Ruta: analizador_cambios/models/cambios.py
Descripción: Define tipos de cambio y su representación en el análisis de código
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Equipo 3
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 28-03-2024
Última Actualización: 29-03-2024

Dependencias:
    - enum.Enum
    - analizador_cambios.core.arbol.nodo.Nodo

Uso:
    from analizador_cambios.models.cambios import TipoCambio, Cambio
    cambio = Cambio(TipoCambio.AGREGADA, nodo_nuevo=nodo)
"""
from enum import Enum

from analizador_cambios.core.arbol.nodo import Nodo


class TipoCambio(Enum):
    """
    Define los tipos de cambios posibles en el análisis.

    Attributes:
        AGREGADA (str): Representa un nodo agregado
        BORRADA (str): Representa un nodo eliminado

    Example:
        >>> tipo = TipoCambio.AGREGADA
        >>> tipo.value
        'agregada'
    """
    AGREGADA = "agregada"
    BORRADA = "borrada"


class Cambio:
    """
    Representa un cambio detectado entre dos versiones de código.

    Almacena información sobre el tipo de cambio y los nodos involucrados.

    Attributes:
        tipo (TipoCambio): Tipo del cambio detectado
        nodo_original (Nodo): Nodo en la versión original
        nodo_nuevo (Nodo): Nodo en la nueva versión
        posicion (int): Posición del cambio en el archivo
        medida_de_cambio (float): Valor numérico del impacto del cambio

    Example:
        >>> cambio = Cambio(TipoCambio.AGREGADA, nodo_nuevo=nodo)
        >>> cambio.tipo
        TipoCambio.AGREGADA
    """
    def __init__(
            self,
            tipo: TipoCambio,
            nodo_original: Nodo = None,
            nodo_nuevo: Nodo = None,
            posicion: int = None,
            medida_de_cambio: float = 0.0):
        # Los nodos pueden ser None dependiendo del tipo de cambio:
        # - Para AGREGADA: solo nodo_nuevo tiene valor
        # - Para BORRADA: solo nodo_original tiene valor
        # - Para MODIFICADA: ambos nodos tienen valor
        self.tipo = tipo
        self.nodo_original = nodo_original
        self.nodo_nuevo = nodo_nuevo
        self.posicion = posicion
        self.medida_de_cambio = medida_de_cambio
