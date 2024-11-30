# comparador_arboles.py
from difflib import SequenceMatcher
from typing import List
from analizador_cambios.core.arbol.nodo import Nodo
from analizador_cambios.models.cambios import TipoCambio, Cambio
from analizador_cambios.models.nodos import TipoNodo

class ComparadorArboles:
    UMBRAL_SIMILITUD = 0.6  # 60% de similitud

    def __init__(self):
        self.cambios: List[Cambio] = []

    def comparar(self, arbol1: Nodo, arbol2: Nodo, espacios_blanco: bool) -> List[Cambio]:
        self.cambios = []
        if espacios_blanco:
            self._comparar_recursivamente_con_espacios(arbol1, arbol2)
        else:
            self._comparar_recursivamente(arbol1, arbol2)
        return self.cambios
        
    def _calcular_similitud(self, str1: str, str2: str) -> float:
        """Calcula el ratio de similitud entre dos strings"""
        return SequenceMatcher(None, str1, str2).ratio()

    def _comparar_recursivamente_con_espacios(self, nodo1: Nodo, nodo2: Nodo):
        # Comparar hijos
        idx1 = 0
        idx2 = 0

        while idx1 < len(nodo1.hijos) and idx2 < len(nodo2.hijos):
            #print(f"idx1: {idx1}, idx2: {idx2}")
            hijo1 = nodo1.hijos[idx1]
            hijo2 = nodo2.hijos[idx2]
            
            similitud = self._calcular_similitud(hijo1.contenido, hijo2.contenido)
            
            if hijo1.contenido == hijo2.contenido:
                #print(f"{hijo1.contenido} == {hijo2.contenido}")
                self._comparar_recursivamente(hijo1, hijo2)
                idx1 += 1
                idx2 += 1
            else:
                #print(f"{hijo1.contenido} != {hijo2.contenido}")
                encontrado = False
                for j in range(idx2 + 1, len(nodo2.hijos)):
                    #print(f"Comparando: {hijo1.contenido} == {nodo2.hijos[j].contenido}")
                    if hijo1.contenido == nodo2.hijos[j].contenido:
                        encontrado = True
                        break
                #print(f"Encontrado: {encontrado}")  
                if encontrado:
                    self.cambios.append(Cambio(TipoCambio.ELIMINADO, hijo1, None, hijo1.numero_nodo))
                    self._todo_modificado(hijo1, None, TipoCambio.ELIMINADO, True)
                    idx1 += 1
                elif similitud >= self.UMBRAL_SIMILITUD:
                    self.cambios.append(Cambio(TipoCambio.MODIFICADO, hijo1, hijo2, hijo1.numero_nodo))
                    self._comparar_recursivamente(hijo1, hijo2)
                    idx1 += 1
                    idx2 += 1
                else:
                    self.cambios.append(Cambio(TipoCambio.AGREGADO, None, hijo2, hijo2.numero_nodo))
                    self._todo_modificado(None, hijo2, TipoCambio.AGREGADO, True)
                    idx2 += 1
                    
        # Procesar restantes
        while idx1 < len(nodo1.hijos):
            self.cambios.append(Cambio(TipoCambio.ELIMINADO, nodo1.hijos[idx1], None, nodo1.hijos[idx1].numero_nodo))
            self._todo_modificado(nodo1.hijos[idx1], None, TipoCambio.ELIMINADO, True)
            idx1 += 1
            
        while idx2 < len(nodo2.hijos):
            self.cambios.append(Cambio(TipoCambio.AGREGADO, None, nodo2.hijos[idx2], nodo2.hijos[idx2].numero_nodo))
            self._todo_modificado(None, nodo2.hijos[idx2], TipoCambio.AGREGADO, True)
            idx2 += 1

    def _comparar_recursivamente(self, nodo1: Nodo, nodo2: Nodo):
        # Comparar hijos
        idx1 = 0
        idx2 = 0

        while idx1 < len(nodo1.hijos) and idx2 < len(nodo2.hijos):
            #print(f"idx1: {idx1}, idx2: {idx2}")
            if nodo1.hijos[idx1].tipo == TipoNodo.WHITE_SPACE:
                idx1 += 1
                continue
            
            if nodo2.hijos[idx2].tipo == TipoNodo.WHITE_SPACE:
                idx2 += 1
                continue

            hijo1 = nodo1.hijos[idx1]
            hijo2 = nodo2.hijos[idx2]
            
            similitud = self._calcular_similitud(hijo1.contenido, hijo2.contenido)
            
            if hijo1.contenido == hijo2.contenido:
                #print(f"{hijo1.contenido} == {hijo2.contenido}")
                self._comparar_recursivamente(hijo1, hijo2)
                idx1 += 1
                idx2 += 1
            else:
                #print(f"{hijo1.contenido} != {hijo2.contenido}")
                encontrado = False
                for j in range(idx2 + 1, len(nodo2.hijos)):
                    #print(f"Comparando: {hijo1.contenido} == {nodo2.hijos[j].contenido}")
                    if nodo2.hijos[j].tipo == TipoNodo.WHITE_SPACE:
                        continue

                    if hijo1.contenido == nodo2.hijos[j].contenido:
                        encontrado = True
                        break
                #print(f"Encontrado: {encontrado}")  
                if encontrado:
                    self.cambios.append(Cambio(TipoCambio.ELIMINADO, hijo1, None, hijo1.numero_nodo))
                    self._todo_modificado(hijo1, None, TipoCambio.ELIMINADO)
                    idx1 += 1
                elif similitud >= self.UMBRAL_SIMILITUD:
                    self.cambios.append(Cambio(TipoCambio.MODIFICADO, hijo1, hijo2, hijo1.numero_nodo))
                    self._comparar_recursivamente(hijo1, hijo2)
                    idx1 += 1
                    idx2 += 1
                else:
                    self.cambios.append(Cambio(TipoCambio.AGREGADO, None, hijo2, hijo2.numero_nodo))
                    self._todo_modificado(None, hijo2, TipoCambio.AGREGADO)
                    idx2 += 1
                    
        # Procesar restantes
        while idx1 < len(nodo1.hijos):
            if nodo1.hijos[idx1].tipo == TipoNodo.WHITE_SPACE:
                idx1 += 1
                continue

            self.cambios.append(Cambio(TipoCambio.ELIMINADO, nodo1.hijos[idx1], None, nodo1.hijos[idx1].numero_nodo))
            self._todo_modificado(nodo1.hijos[idx1], None, TipoCambio.ELIMINADO)
            idx1 += 1
            
        while idx2 < len(nodo2.hijos):
            if nodo2.hijos[idx2].tipo == TipoNodo.WHITE_SPACE:
                idx2 += 1
                continue

            self.cambios.append(Cambio(TipoCambio.AGREGADO, None, nodo2.hijos[idx2], nodo2.hijos[idx2].numero_nodo))
            self._todo_modificado(None, nodo2.hijos[idx2], TipoCambio.AGREGADO)
            idx2 += 1

    def _todo_modificado(self, nodo1: Nodo | None, nodo2: Nodo | None, tipo: TipoCambio, espacios_blanco: bool = False):
        if nodo1 is not None:
            for hijo in nodo1.hijos:
                if hijo.tipo == TipoNodo.WHITE_SPACE and not espacios_blanco:
                    continue

                self.cambios.append(Cambio(tipo, hijo, None, hijo.numero_nodo))
                if hijo.hijos:
                    self._todo_modificado(hijo, None, tipo)
        elif nodo2 is not None:
            for hijo in nodo2.hijos:
                if hijo.tipo == TipoNodo.WHITE_SPACE and not espacios_blanco:
                    continue

                self.cambios.append(Cambio(tipo, None, hijo, hijo.numero_nodo))
                if hijo.hijos:
                    self._todo_modificado(None, hijo, tipo)