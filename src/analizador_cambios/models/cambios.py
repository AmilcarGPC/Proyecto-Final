# models/cambios.py
from enum import Enum
from analizador_cambios.core.arbol.nodo import Nodo

class TipoCambio(Enum):
    AGREGADA = "agregada" 
    BORRADA = "borrada"

class Cambio:
    def __init__(self, tipo: TipoCambio, nodo_original: Nodo =None, nodo_nuevo: Nodo=None, posicion: int=None, medida_de_cambio: float= 0.0):
        self.tipo = tipo
        self.nodo_original = nodo_original
        self.nodo_nuevo = nodo_nuevo
        self.posicion = posicion
        self.medida_de_cambio = medida_de_cambio