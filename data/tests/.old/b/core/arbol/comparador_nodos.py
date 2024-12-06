# comparador_nodos.py
from analizador_cambios.core.arbol.nodo import Nodo
from analizador_cambios.models.cambios import TipoCambio

class ComparadorNodos:
    @staticmethod
    def comparar(nodo1: Nodo, nodo2: Nodo) -> TipoCambio:
        """
        Compara dos nodos y determina el tipo de cambio
        """
        if nodo1.tipo != nodo2.tipo:
            return TipoCambio.MODIFICADO
        if nodo1.contenido != nodo2.contenido:
            return TipoCambio.MODIFICADO
        return TipoCambio.SIN_CAMBIOS