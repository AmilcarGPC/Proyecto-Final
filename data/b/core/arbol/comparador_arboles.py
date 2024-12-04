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
        self.taked_agregado = {}
        self.taked_eliminado = {}

    def comparar(self, arbol1: Nodo, arbol2: Nodo, espacios_blanco: bool) -> List[Cambio]:
        self.cambios = []
        if espacios_blanco:
            self._comparar_recursivamente_con_espacios(arbol1, arbol2)
        else:
            self._comparar_recursivamente(arbol1, arbol2)
        return self.cambios
        
    def _calcular_similitud(self, str1: str, str2: str) -> float:
        return SequenceMatcher(None, str1, str2).ratio()

    def _comparar_recursivamente_con_espacios(self, nodo1: Nodo, nodo2: Nodo):
        return 0

    def _comparar_recursivamente(self, nodo1: Nodo, nodo2: Nodo):
        # Comparar hijos
        idx1 = 0
        idx2 = 0

        a_eliminar_totalmente = []
        a_agregar_totalmente = []

        # Recorrer nodos
        while idx1 < len(nodo1.hijos) and idx2 < len(nodo2.hijos):
            
            # Ignorar espacios en blanco
            if nodo1.hijos[idx1].tipo == TipoNodo.WHITE_SPACE:
                idx1 += 1
                continue
            
            # Ignorar espacios en blanco
            if nodo2.hijos[idx2].tipo == TipoNodo.WHITE_SPACE:
                idx2 += 1
                continue
                
            hijo1 = nodo1.hijos[idx1]
            hijo2 = nodo2.hijos[idx2]
            
            similitud = self._calcular_similitud(hijo1.contenido, hijo2.contenido)
            
            if hijo1.contenido == hijo2.contenido: # Si los nodos son iguales, comparar recursivamente y avanzar
                self._comparar_recursivamente(hijo1, hijo2)
                idx1 += 1
                idx2 += 1
            else: # Si los nodos son diferentes, buscar si estos fueron eliminados o modificados
                decision = self._existe_en_v1(nodo1, nodo2, idx1, idx2) # Se busca si el nodo de la versión 1 se encuentra en la versión 2
                if decision:
                    encontrado = self._encontrar_en_v2(nodo1, nodo2, idx1, idx2) # Se busca si el nodo de la versión 1 se algún punto de la versión 2

                    if encontrado[0]:
                        # Si se encontró, se considera que fue desplazado, por lo que se elimina y se añadé posteriormente
                        self.cambios.append(Cambio(TipoCambio.BORRADA, hijo1, None, hijo1.numero_nodo))
                        self._todo_modificado(hijo1, None, TipoCambio.BORRADA)
                        idx1 += 1
                    elif similitud >= self.UMBRAL_SIMILITUD: 
                        # Si la similitud es mayor al umbral, se considera que pudo haber sido modificado                       
                        if not self._encontrar_similar(nodo1, nodo2, idx1, idx2-1):
                            # Se asegura que el nodo candidato de la versión 2 no se encuentre en la versión 1
                            self.cambios.append(Cambio(TipoCambio.BORRADA, hijo1, None, hijo1.numero_nodo))
                            a_eliminar_totalmente.append(hijo1)
                            self._todo_modificado(hijo1, None, TipoCambio.BORRADA)
                            idx1 += 1
                        else:
                            self.cambios.append(Cambio(TipoCambio.BORRADA, hijo1, hijo2, hijo1.numero_nodo, round(similitud, 2)))
                            self.cambios.append(Cambio(TipoCambio.AGREGADA, hijo1, hijo2, hijo2.numero_nodo, round(similitud, 2)))
                            self._comparar_recursivamente(hijo1, hijo2)
                            idx1 += 1
                            idx2 += 1
                    else: # Si no se encontró, se considera que fue eliminado
                        if not self._encontrar_similar(nodo1, nodo2, idx1, idx2): # Se busca si el nodo de la versión 1 se encuentra en la versión 2 por similitud
                            self.cambios.append(Cambio(TipoCambio.BORRADA, hijo1, None, hijo1.numero_nodo))
                            a_eliminar_totalmente.append(hijo1)
                            self._todo_modificado(hijo1, None, TipoCambio.BORRADA)
                            idx1 += 1
                        else:
                            idx2 += 1
                else:
                    idx2 += 1     
        # Procesar restantes
        while idx1 < len(nodo1.hijos): # Se recorren los nodos restantes de la versión 1
            if nodo1.hijos[idx1].tipo == TipoNodo.WHITE_SPACE:
                idx1 += 1
                continue
            # Si el nodo de la versión 1 no se encuentra en la versión 2, se considera que fue eliminado
            self.cambios.append(Cambio(TipoCambio.BORRADA, nodo1.hijos[idx1], None, nodo1.hijos[idx1].numero_nodo))
            self._todo_modificado(nodo1.hijos[idx1], None, TipoCambio.BORRADA)
            idx1 += 1
            
        while idx2 < len(nodo2.hijos): # Se recorren los nodos restantes de la versión 2
            if nodo2.hijos[idx2].tipo == TipoNodo.WHITE_SPACE:
                idx2 += 1
                continue
            # Si el nodo de la versión 2 no se encuentra en la versión 1, se considera que fue agregado
            self.cambios.append(Cambio(TipoCambio.AGREGADA, None, nodo2.hijos[idx2], nodo2.hijos[idx2].numero_nodo))
            self._todo_modificado(None, nodo2.hijos[idx2], TipoCambio.AGREGADA)
            idx2 += 1

    def _existe_en_v1(self, nodo1, nodo2, idx1, idx2):
        hijo2 = nodo2.hijos[idx2] # Se toma un nodo de la versión 2
        similitud_encontrada = False
        for j in range(idx1, len(nodo1.hijos)): # Se recorren los nodos de la versión 1
            if nodo1.hijos[j].numero_nodo in self.taked_agregado:
                if self.taked_agregado[nodo1.hijos[j].numero_nodo] == hijo2.numero_nodo:
                    similitud_encontrada = True
                    break
            elif hijo2.contenido == nodo1.hijos[j].contenido: # Si los dos nodos son iguales, se considera que hubo un desplazamiento
                # Si el nodo de la versión 2 se encontró en la última posición de la versión 1, quiere decir que se desplazó desde el final de la versión 1 al inicio de la versión 2
                if j == len(nodo1.hijos) - 1 and idx1 == 0:
                    self.cambios.append(Cambio(TipoCambio.AGREGADA, None, hijo2, hijo2.numero_nodo))
                    self._todo_modificado(None, hijo2, TipoCambio.AGREGADA)
                    return False
                
                similitud_encontrada = True
                self.taked_agregado[nodo1.hijos[j].numero_nodo] = hijo2.numero_nodo

                break
        # Si no se encontró explícitamente, se busca por similitud  
        if not similitud_encontrada:
            similitud_temporal_encontrada = False
            for j in range(idx1, len(nodo1.hijos)): # Se recorren los nodos de la versión 1
                similitud_temporal = self._calcular_similitud(hijo2.contenido, nodo1.hijos[j].contenido) # Se calcula la similitud entre el nodo de la versión 2 y el nodo de la versión 1
                if (similitud_temporal >= self.UMBRAL_SIMILITUD) and (nodo1.hijos[j].numero_nodo not in self.taked_agregado): # Si la similitud es mayor al umbral
                    # Si dicho nodo similar de la versión 1 no se encuentra explícitamente en la versión 2, quiere decir que fue modificado y se convirtió en el nodo de la versión 2
                    if not self.existe_explicito(nodo1.hijos[j], nodo2):
                        similitud_temporal_encontrada = True
                        self.taked_agregado[nodo1.hijos[j].numero_nodo] = hijo2.numero_nodo
                        break
            # El nodo de la versión 2 no se encuentra en la versión 1 por similitud

            # Si no se encontró explícitamente ni por similitud, se considera que fue agregado al 100%
            if not similitud_temporal_encontrada:
                self.cambios.append(Cambio(TipoCambio.AGREGADA, None, hijo2, hijo2.numero_nodo))
                self._todo_modificado(None, hijo2, TipoCambio.AGREGADA)
                return False
        return True
    
    def existe_explicito(self, hijo, nodo):
        for j in range(0, len(nodo.hijos)): # Se recorren los nodos
            if hijo.contenido == nodo.hijos[j].contenido: # Se determina si este existe explícitamente
                return True
        return False
    
    def _encontrar_en_v2(self, nodo1, nodo2, idx1, idx2):
        hijo1 = nodo1.hijos[idx1]
        for j in range(idx2 + 1, len(nodo2.hijos)): # Se recorren los nodos de la versión 2
            if nodo2.hijos[j].tipo == TipoNodo.WHITE_SPACE: # Se ignora los espacios en blanco
                continue

            # Si el nodo de la versión 1 se encuentra en la versión 2, se considera que fue desplazado
            if (hijo1.contenido == nodo2.hijos[j].contenido) and (nodo2.hijos[j].numero_nodo not in self.taked_eliminado):
                self.taked_eliminado[nodo2.hijos[j].numero_nodo] = hijo1.numero_nodo
                return (True, nodo2.hijos[j].numero_nodo)
            
            # El nodo de la versión 1 no se encuentra en la versión 2 explícitamente
        return (False, None)
    
    def _encontrar_similar(self, nodo1, nodo2, idx1, idx2):
        hijo1 = nodo1.hijos[idx1]
        for j in range(idx2 + 1, len(nodo2.hijos)): # Se recorren los nodos de la versión 2
            if nodo2.hijos[j].tipo == TipoNodo.WHITE_SPACE: # Se ignora los espacios en blanco
                continue

            similitud = self._calcular_similitud(hijo1.contenido, nodo2.hijos[j].contenido) # Se calcula la similitud entre el nodo de la versión 1 y el nodo de la versión 2
            if (similitud >= self.UMBRAL_SIMILITUD) and (nodo2.hijos[j].numero_nodo not in self.taked_eliminado): # Si la similitud es mayor al umbral

                # Si dicho nodo similar de la versión 2 no se encuentra explícitamente en la versión 1, quiere decir que fue modificado y se convirtió en el nodo de la versión 1
                if not self.existe_explicito(nodo2.hijos[j], nodo1):
                    self.taked_eliminado[nodo2.hijos[j].numero_nodo] = hijo1.numero_nodo
                    return True
                
        # El nodo de la versión 1 no se encuentra en la versión 2 por similitud
        return False

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