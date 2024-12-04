"""
Nombre del módulo: comparador_principal.py
Ruta: analizador_cambios/core/arbol/comparador_principal.py
Descripción: Compara versiones de archivos Python y contabiliza cambios
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 28-11-2024
Última Actualización: 02-12-2024

Dependencias:
    - typing.List
    - typing.Union
    - analizador_cambios.models.cambios
    - analizador_cambios.core.arbol.arbol_sintactico
    - analizador_cambios.core.arbol.comparador_arboles

Uso:
    from analizador_cambios.core.arbol.comparador_principal import (
        ComparadorVersiones
    )
    comparador = ComparadorVersiones()
    cambios = comparador.comparar_archivos(arbol1, arbol2)
"""

from typing import List, Union

from analizador_cambios.models.cambios import Cambio, TipoCambio
from analizador_cambios.core.arbol.arbol_sintactico import ArbolArchivoPython
from analizador_cambios.core.arbol.comparador_arboles import ComparadorArboles


class ComparadorVersiones:
    """
    Compara versiones de archivos Python y contabiliza sus diferencias.

    Procesa árboles sintácticos y genera reportes de cambios entre versiones.

    Attributes:
        comparador (ComparadorArboles): Instancia para comparar árboles

    Methods:
        comparar_archivos(arbol_v1: ArbolArchivoPython,
                          arbol_v2: ArbolArchivoPython) -> List[Cambio]:
            Compara dos versiones de un archivo y devuelve los cambios hallados

        contar_cambios(cambios: List[Cambio]) -> Union[int, int, int]:
            Cuenta la cantidad de cambios en un reporte

    Example:
        >>> comparador = ComparadorVersiones()
        >>> cambios = comparador.comparar_archivos(arbol1, arbol2)
    """
    def __init__(self):
        self.comparador = ComparadorArboles()

    def comparar_archivos(
            self,
            arbol_v1: ArbolArchivoPython,
            arbol_v2: ArbolArchivoPython) -> List[Cambio]:
        """
        Compara dos versiones de un archivo y retorna sus diferencias.

        Args:
            arbol_v1 (ArbolArchivoPython): Árbol de la versión original
            arbol_v2 (ArbolArchivoPython): Árbol de la nueva versión
            espacios_blanco (bool): Incluir cambios en espacios

        Returns:
            str: Reporte formateado de diferencias

        Example:
            >>> comparar_archivos(arbol1, arbol2)
        """
        cambios = self.comparador.comparar(
            arbol_v1.raiz,
            arbol_v2.raiz
        )
        return cambios

    def contar_cambios(
            self,
            cambios: List[Cambio]) -> Union[int, int, int]:
        """
        Calcula la cantidad de cambios por tipo en un reporte.

        Args:
            cambios (List[Cambio]): Lista de cambios a contabilizar

        Returns:
            Tuple[int, int, int]: Cantidad de líneas (agregadas, 
                                 modificadas, borradas)

        Example:
            >>> contar_cambios(lista_cambios)
            (5, 2, 3)
        """
        if not cambios:
            return 0, 0, 0

        cantidad_agregadas = 0
        cantidad_agregadas_modificadas = 0
        cantidad_borradas = 0

        for cambio in cambios:
            # Ignoramos cambios con medida 1.0 (100%) ya que representan líneas
            # sin modificaciones reales
            if int(cambio.medida_de_cambio * 100) == 100:
                continue

            # La medida de cambio determina si una línea agregada fue
            # completamente nueva (0.0) o modificada parcialmente
            if cambio.tipo == TipoCambio.AGREGADA:
                if int(cambio.medida_de_cambio * 100) != 0:
                    cantidad_agregadas_modificadas += 1
                else:
                    cantidad_agregadas += 1
            elif cambio.tipo == TipoCambio.BORRADA:
                cantidad_borradas += 1

        return (
            cantidad_agregadas,
            cantidad_agregadas_modificadas,
            cantidad_borradas
        )
