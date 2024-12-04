"""
Nombre del módulo: comparador_arboles.py
Ruta: analizador_cambios/core/arbol/comparador_arboles.py
Descripción: Compara árboles sintácticos y detecta cambios entre versiones
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 28-11-2024
Última Actualización: 03-12-2024

Dependencias:
    - difflib.SequenceMatcher
    - typing.List
    - analizador_cambios.config.umbral
    - analizador_cambios.core.arbol.nodo
    - analizador_cambios.models.cambios

Uso:
    from analizador_cambios.core.arbol.comparador_arboles import (
        ComparadorArboles
    )
    comparador = ComparadorArboles()
    cambios = comparador.comparar(arbol1, arbol2)
"""
from difflib import SequenceMatcher
from typing import List

from analizador_cambios.config.umbral import UMBRAL_SIMILITUD
from analizador_cambios.core.arbol.nodo import Nodo
from analizador_cambios.models.cambios import TipoCambio, Cambio
from contador_lineas.models.nodos import TipoNodo


class ComparadorArboles:
    """
    Compara árboles sintácticos y detecta diferencias entre versiones.

    Attributes:
        cambios (List[Cambio]): Lista de cambios detectados
        nodos_agregados (dict): Mapeo de nodos agregados
        nodos_eliminados (dict): Mapeo de nodos eliminados

    Methods:
        comparar(arbol1: Nodo, arbol2: Nodo) -> List[Cambio]:
            Compara dos árboles y devuelve los cambios detectados

    Example:
        >>> comparador = ComparadorArboles()
        >>> cambios = comparador.comparar(arbol1, arbol2)
    """
    def __init__(self):
        self.cambios: List[Cambio] = []
        self.nodos_agregados = {}
        self.nodos_eliminados = {}

    def comparar(
            self,
            arbol1: Nodo,
            arbol2: Nodo) -> List[Cambio]:
        """
        Compara dos árboles y retorna lista de cambios.

        Args:
            arbol1 (Nodo): Árbol de versión original
            arbol2 (Nodo): Árbol de versión nueva

        Returns:
            List[Cambio]: Lista de cambios detectados

        Example:
            >>> comparar(arbol1, arbol2)
        """
        self.cambios = []
        self._comparar_recursivamente(arbol1, arbol2)

        return self.cambios

    def _calcular_similitud(self, str1: str, str2: str) -> float:
        """
        Calcula ratio de similitud entre dos cadenas.

        Args:
            str1 (str): Primera cadena
            str2 (str): Segunda cadena

        Returns:
            float: Ratio de similitud entre 0 y 1

        Example:
            >>> _calcular_similitud("abc", "abd")
        """
        return SequenceMatcher(None, str1, str2).ratio()

    def _comparar_recursivamente(self, nodo1: Nodo, nodo2: Nodo):
        """
        Compara recursivamente dos nodos y sus subárboles.

        Args:
            nodo1 (Nodo): Nodo del árbol original
            nodo2 (Nodo): Nodo del árbol modificado

        Example:
            >>> _comparar_recursivamente(nodo1, nodo2)
        """
        # Comparar hijos
        idx1 = 0
        idx2 = 0

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

            similitud = self._calcular_similitud(
                    hijo1.contenido,
                    hijo2.contenido
                )

            # Si los nodos son iguales, comparar recursivamente y avanzar
            if hijo1.contenido == hijo2.contenido:
                self._comparar_recursivamente(hijo1, hijo2)
                idx1 += 1
                idx2 += 1
            else:
                # Si los nodos son diferentes, buscar si estos fueron eliminados
                # o modificados

                # Se busca si el nodo de la versión 1 se encuentra en la
                # versión 2
                decision = self._existe_en_version_original(
                        nodo1,
                        nodo2,
                        idx1,
                        idx2
                    )

                if decision:
                    # Se busca si el nodo de la versión 1 se algún punto de la
                    # versión 2
                    encontrado = self._encontrar_en_version_nueva(
                            nodo1,
                            nodo2,
                            idx1,
                            idx2
                        )

                    if encontrado[0]:
                        # Si se encontró, se considera que fue desplazado,
                        # por lo que se elimina y se añadé posteriormente
                        self.cambios.append(Cambio(
                                TipoCambio.BORRADA,
                                hijo1,
                                None,
                                hijo1.numero_nodo
                            ))
                        self._todo_modificado(hijo1, None, TipoCambio.BORRADA)
                        idx1 += 1
                    elif similitud >= UMBRAL_SIMILITUD:
                        # Si la similitud es mayor al umbral, se considera que
                        # pudo haber sido modificado
                        if not self._encontrar_similar(
                                nodo1,
                                nodo2,
                                idx1,
                                idx2-1
                            ):
                            # Se asegura que el nodo candidato de la versión 2
                            # no se encuentre en la versión 1
                            self.cambios.append(Cambio(
                                    TipoCambio.BORRADA,
                                    hijo1,
                                    None,
                                    hijo1.numero_nodo
                                ))
                            self._todo_modificado(
                                    hijo1,
                                    None,
                                    TipoCambio.BORRADA
                                )
                            idx1 += 1
                        else:
                            self.cambios.append(Cambio(
                                    TipoCambio.BORRADA,
                                    hijo1,
                                    hijo2,
                                    hijo1.numero_nodo,
                                    round(similitud, 2)
                                ))
                            self.cambios.append(Cambio(
                                    TipoCambio.AGREGADA,
                                    hijo1,
                                    hijo2,
                                    hijo2.numero_nodo,
                                    round(similitud, 2)
                                ))
                            self._comparar_recursivamente(hijo1, hijo2)
                            idx1 += 1
                            idx2 += 1
                    else:
                        # Si no se encontró, se considera que fue eliminado
                        # Se busca si el nodo de la versión 1 se encuentra en la
                        # versión 2 por similitud
                        if not self._encontrar_similar(
                                nodo1,
                                nodo2,
                                idx1,
                                idx2
                            ):
                            self.cambios.append(Cambio(
                                    TipoCambio.BORRADA,
                                    hijo1,
                                    None,
                                    hijo1.numero_nodo
                                ))
                            self._todo_modificado(
                                    hijo1,
                                    None,
                                    TipoCambio.BORRADA
                                )
                            idx1 += 1
                        else:
                            self.cambios.append(Cambio(
                                    TipoCambio.AGREGADA,
                                    hijo1,
                                    hijo2,
                                    hijo2.numero_nodo
                                ))
                            self._todo_modificado(
                                    None,
                                    hijo2,
                                    TipoCambio.AGREGADA
                                )
                            idx2 += 1
                else:
                    idx2 += 1

        # Procesar restantes

        # Se recorren los nodos restantes de la versión 1
        while idx1 < len(nodo1.hijos):
            if nodo1.hijos[idx1].tipo == TipoNodo.WHITE_SPACE:
                idx1 += 1
                continue
            # Si el nodo de la versión 1 no se encuentra en la versión 2, se
            # considera que fue eliminado
            self.cambios.append(Cambio(
                    TipoCambio.BORRADA,
                    nodo1.hijos[idx1],
                    None,
                    nodo1.hijos[idx1].numero_nodo
                ))
            self._todo_modificado(nodo1.hijos[idx1], None, TipoCambio.BORRADA)
            idx1 += 1

        # Se recorren los nodos restantes de la versión 2
        while idx2 < len(nodo2.hijos):
            if nodo2.hijos[idx2].tipo == TipoNodo.WHITE_SPACE:
                idx2 += 1
                continue
            # Si el nodo de la versión 2 no se encuentra en la versión 1, se
            # considera que fue agregado
            self.cambios.append(Cambio(
                    TipoCambio.AGREGADA,
                    None,
                    nodo2.hijos[idx2],
                    nodo2.hijos[idx2].numero_nodo
                ))
            self._todo_modificado(None, nodo2.hijos[idx2], TipoCambio.AGREGADA)
            idx2 += 1

    def _existe_en_version_original(self, nodo1, nodo2, idx1, idx2) -> bool:
        """
        Verifica si un nodo existe en la versión original.

        Args:
            nodo1 (Nodo): Nodo raíz original
            nodo2 (Nodo): Nodo raíz modificado
            idx1 (int): Índice en árbol original
            idx2 (int): Índice en árbol modificado

        Returns:
            bool: True si existe en versión original

        Example:
            >>> _existe_en_version_original(nodo1, nodo2, 0, 0)
        """
        hijo2 = nodo2.hijos[idx2] # Se toma un nodo de la versión 2
        similitud_encontrada = False

        # Se recorren los nodos de la versión 1
        for j in range(idx1, len(nodo1.hijos)):
            if nodo1.hijos[j].numero_nodo in self.nodos_agregados:
                if self.nodos_agregados[nodo1.hijos[j].numero_nodo] == \
                hijo2.numero_nodo:
                    similitud_encontrada = True
                    break
            elif hijo2.contenido == nodo1.hijos[j].contenido:
                # Si los dos nodos son iguales, se considera que hubo un
                # desplazamiento

                # Si el nodo de la versión 2 se encontró en la última posición
                # de la versión 1, quiere decir que se desplazó desde el final
                # de la versión 1 al inicio de la versión 2
                if j == len(nodo1.hijos) - 1 and idx1 == 0:
                    self.cambios.append(Cambio(
                            TipoCambio.AGREGADA,
                            None,
                            hijo2,
                            hijo2.numero_nodo
                        ))
                    self._todo_modificado(None, hijo2, TipoCambio.AGREGADA)
                    return False

                similitud_encontrada = True
                self.nodos_agregados[nodo1.hijos[j].numero_nodo] = \
                hijo2.numero_nodo
                break

        # Si no se encontró explícitamente, se busca por similitud
        if not similitud_encontrada:
            similitud_temporal_encontrada = False

            # Se recorren los nodos de la versión 1
            for j in range(idx1, len(nodo1.hijos)):
                # Se calcula la similitud entre el nodo de la versión 2 y el
                # nodo de la versión 1
                similitud_temporal = self._calcular_similitud(
                        hijo2.contenido,
                        nodo1.hijos[j].contenido
                    )

                if (similitud_temporal >= UMBRAL_SIMILITUD) and \
                    (nodo1.hijos[j].numero_nodo not in self.nodos_agregados):
                    # Si dicho nodo similar de la versión 1 no se encuentra
                    # explícitamente en la versión 2, quiere decir que fue
                    # modificado y se convirtió en el nodo de la versión 2
                    if not self._existe_explicito(nodo1.hijos[j], nodo2):
                        similitud_temporal_encontrada = True
                        self.nodos_agregados[nodo1.hijos[j].numero_nodo] = \
                        hijo2.numero_nodo
                        break
            # El nodo de la versión 2 no se encuentra en la versión 1 por
            # similitud

            # Si no se encontró explícitamente ni por similitud, se considera
            # que fue agregado al 100%
            if not similitud_temporal_encontrada:
                self.cambios.append(Cambio(
                        TipoCambio.AGREGADA,
                        None,
                        hijo2,
                        hijo2.numero_nodo
                    ))
                self._todo_modificado(None, hijo2, TipoCambio.AGREGADA)
                return False

        return True

    def _existe_explicito(self, hijo, nodo) -> bool:
        """
        Verifica si un nodo existe explícitamente en el árbol.

        Args:
            hijo (Nodo): Nodo a buscar
            nodo (Nodo): Nodo raíz

        Returns:
            bool: True si existe explícitamente

        Example:
            >>> _existe_explicito(hijo, nodo)
        """
        # Se recorren los nodos
        for j in range(0,len(nodo.hijos)):
            # Se determina si este existe explícitamente
            if hijo.contenido == nodo.hijos[j].contenido:
                return True
        return False

    def _encontrar_en_version_nueva(self, nodo1, nodo2, idx1, idx2) -> bool:
        """
        Busca un nodo en la versión nueva del árbol.

        Args:
            nodo1 (Nodo): Nodo raíz original
            nodo2 (Nodo): Nodo raíz modificado 
            idx1 (int): Índice en árbol original
            idx2 (int): Índice en árbol modificado

        Returns:
            bool: True si encuentra el nodo

        Example:
            >>> _encontrar_en_version_nueva(nodo1, nodo2, 0, 0)
        """
        hijo1 = nodo1.hijos[idx1]

        # Se recorren los nodos de la versión 2
        for j in range(idx2 + 1, len(nodo2.hijos)):
            # Se ignora los espacios en blanco
            if nodo2.hijos[j].tipo == TipoNodo.WHITE_SPACE:
                continue

            # Si el nodo de la versión 1 se encuentra en la versión 2, se
            # considera que fue desplazado
            if (hijo1.contenido == nodo2.hijos[j].contenido) and \
            (nodo2.hijos[j].numero_nodo not in self.nodos_eliminados):
                self.nodos_eliminados[nodo2.hijos[j].numero_nodo] = \
                hijo1.numero_nodo
                return (True, nodo2.hijos[j].numero_nodo)

            # El nodo de la versión 1 no se encuentra en la versión 2
            # explícitamente
        return (False, None)

    def _encontrar_similar(self, nodo1, nodo2, idx1, idx2) -> bool:
        """
        Busca un nodo similar en un rango de nodos.

        Args:
            nodo1 (Nodo): Nodo raíz original
            nodo2 (Nodo): Nodo raíz modificado 
            idx1 (int): Índice en árbol original
            idx2 (int): Índice en árbol modificado

        Returns:
            bool: True si encuentra un nodo similar

        Example:
            >>> _encontrar_similar(nodo1, nodo2, 0, 0)
        """
        hijo1 = nodo1.hijos[idx1]

        # Se recorren los nodos de la versión 2
        for j in range(idx2 + 1, len(nodo2.hijos)):
            # Se ignora los espacios en blanco
            if nodo2.hijos[j].tipo == TipoNodo.WHITE_SPACE:
                continue

            # Se calcula la similitud entre el nodo de la versión 1 y el nodo de
            # la versión 2
            similitud = self._calcular_similitud(
                    hijo1.contenido,
                    nodo2.hijos[j].contenido
                )

            if (similitud >= UMBRAL_SIMILITUD) and \
            (nodo2.hijos[j].numero_nodo not in self.nodos_eliminados):
                # Si dicho nodo similar de la versión 2 no se encuentra
                # explícitamente en la versión 1, quiere decir que fue
                # modificado y se convirtió en el nodo de la versión 1
                if not self._existe_explicito(nodo2.hijos[j], nodo1):
                    self.nodos_eliminados[nodo2.hijos[j].numero_nodo] = \
                    hijo1.numero_nodo
                    return True

        # El nodo de la versión 1 no se encuentra en la versión 2 por similitud
        return False

    def _todo_modificado(
            self,
            nodo1: Nodo | None,
            nodo2: Nodo | None,
            tipo: TipoCambio) -> None:
        """
        Marca todos los hijos de un nodo como modificados.

        Args:
            nodo1 (Nodo): Nodo de la versión original
            nodo2 (Nodo): Nodo de la versión modificada
            tipo (TipoCambio): Tipo de cambio

        Example:
            >>> _todo_modificado(nodo1, nodo2, TipoCambio.MODIFICADA)
        """
        if nodo1 is not None:
            for hijo in nodo1.hijos:
                if hijo.tipo == TipoNodo.WHITE_SPACE:
                    continue

                self.cambios.append(Cambio(tipo, hijo, None, hijo.numero_nodo))
                if hijo.hijos:
                    self._todo_modificado(hijo, None, tipo)
        elif nodo2 is not None:
            for hijo in nodo2.hijos:
                if hijo.tipo == TipoNodo.WHITE_SPACE:
                    continue

                self.cambios.append(Cambio(tipo, None, hijo, hijo.numero_nodo))
                if hijo.hijos:
                    self._todo_modificado(None, hijo, tipo)
