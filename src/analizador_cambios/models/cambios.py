# models/cambios.py
from enum import Enum

class TipoCambio(Enum):
    SIN_CAMBIOS = "sin_cambios"
    AGREGADO = "agregado" 
    ELIMINADO = "eliminado"
    MODIFICADO = "modificado"

class Cambio:
    def __init__(self, tipo: TipoCambio, nodo_original=None, nodo_nuevo=None, posicion=None):
        self.tipo = tipo
        self.nodo_original = nodo_original
        self.nodo_nuevo = nodo_nuevo
        self.posicion = posicion