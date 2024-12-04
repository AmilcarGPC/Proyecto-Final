"""
Nombre del módulo: escribir_cambios.py
Ruta: analizador_cambios/core/gestion_archivos/escribir_cambios.py
Descripción: Procesa y comenta cambios entre versiones de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 28-11-2024
Última Actualización: 30-11-2024

Dependencias:
    - typing.List, Tuple
    - analizador_cambios.core.contadores.analizador
    - analizador_cambios.models.cambios

Uso:
    from analizador_cambios.core.gestion_archivos.escribir_cambios import (
        EscribirCambios
    )
    escritor = EscribirCambios()
    codigo1, codigo2 = escritor.escribir(analisis1, analisis2, cambios)
"""

from typing import List, Tuple

from analizador_cambios.core.contadores.analizador import AnalizadorCodigo
from analizador_cambios.models.cambios import TipoCambio
from analizador_cambios.models.cambios import Cambio


class EscribirCambios:
    """
    Procesa y comenta cambios detectados entre versiones de código.

    Attributes:
        None

    Methods:
        escribir(analisis_1: AnalizadorCodigo,
                analisis_2: AnalizadorCodigo,
                cambios: List[Cambio]) -> Tuple[List[str], List[str]]:
            Comenta los cambios detectados en los códigos originales

    Example:
        >>> escritor = EscribirCambios()
        >>> codigo1, codigo2 = escritor.escribir(analisis1, analisis2, cambios)
    """

    def escribir(
            self,
            analisis_1: AnalizadorCodigo,
            analisis_2: AnalizadorCodigo,
            cambios: List[Cambio]) -> Tuple[List[str], List[str]]:
        """
        Procesa códigos y agrega comentarios sobre cambios.

        Args:
            analisis_1 (AnalizadorCodigo): Análisis de versión original
            analisis_2 (AnalizadorCodigo): Análisis de versión nueva
            cambios (List[Cambio]): Lista de cambios detectados

        Returns:
            Tuple[List[str], List[str]]: Códigos comentados

        Example:
            >>> escribir(analisis1, analisis2, cambios)
        """
        codigo1 = analisis_1.codigo
        codigo2 = analisis_2.codigo

        for cambio in cambios:
            # Ignoramos cambios con medida 1.0 (100%) ya que representan líneas
            # sin modificaciones reales
            if self._es_cambio_significativo(cambio):
                self._procesar_cambio(
                    cambio,
                    codigo1,
                    codigo2,
                    analisis_1.arbol.mapeo_lineas,
                    analisis_2.arbol.mapeo_lineas
                )

        return codigo1, codigo2

    def _es_cambio_significativo(self, cambio: Cambio) -> bool:
        """
        Verifica si un cambio tiene impacto significativo.

        Args:
            cambio (Cambio): Cambio a verificar

        Returns:
            bool: True si el cambio es significativo

        Example:
            >>> _es_cambio_significativo(cambio)
        """
        return int(cambio.medida_de_cambio*100) != 100

    def _procesar_cambio(
            self,
            cambio: Cambio,
            codigo1: List[str],
            codigo2: List[str],
            mapeo_original: List[int],
            mapeo_nuevo: List[int]) -> None:
        """
        Procesa un cambio específico y actualiza los códigos.

        Args:
            cambio (Cambio): Cambio a procesar
            codigo1 (List[str]): Código original
            codigo2 (List[str]): Código nuevo
            mapeo_original (List[int]): Mapeo de líneas original
            mapeo_nuevo (List[int]): Mapeo de líneas nuevo

        Example:
            >>> _procesar_cambio(cambio, codigo1, codigo2, mapeo1, mapeo2)
        """
        if cambio.tipo == TipoCambio.BORRADA:
            self._procesar_borrado(cambio, codigo1, mapeo_original)
        elif cambio.tipo == TipoCambio.AGREGADA:
            self._procesar_agregado(cambio, codigo2, mapeo_nuevo)

    def _procesar_borrado(
            self,
            cambio: Cambio,
            codigo: List[str],
            mapeo: dict) -> None:
        """
        Procesa una línea borrada y agrega comentario.

        Args:
            cambio (Cambio): Cambio de tipo borrado
            codigo (List[str]): Código a modificar
            mapeo (dict): Mapeo de líneas

        Example:
            >>> _procesar_borrado(cambio, codigo, mapeo)
        """
        linea = mapeo[cambio.posicion][-1]
        ajuste = self._obtener_ajuste_multilinea(
            mapeo[cambio.posicion]
        )
        comentario = f"{codigo[linea].rstrip()} # BORRADA"
        codigo[linea] = comentario + ajuste

    def _procesar_agregado(
            self,
            cambio: Cambio,
            codigo: List[str],
            mapeo: dict) -> None:
        """
        Procesa una línea agregada y agrega comentario.

        Args:
            cambio (Cambio): Cambio de tipo agregado
            codigo (List[str]): Código a modificar
            mapeo (dict): Mapeo de líneas

        Example:
            >>> _procesar_agregado(cambio, codigo, mapeo)
        """
        linea = mapeo[cambio.posicion][-1]
        ajuste = self._obtener_ajuste_multilinea(
            mapeo[cambio.posicion]
        )
        # La medida de cambio determina si una línea agregada fue
        # completamente nueva (0.0) o modificada parcialmente
        # Esto ayuda a diferenciar entre código nuevo y modificaciones
        if int(cambio.medida_de_cambio*100) != 0:
            comentario = f"{codigo[linea].rstrip()}" + " # AÑADIDA EN UN " + \
            f"{cambio.medida_de_cambio}%"
        else:
            comentario = f"{codigo[linea].rstrip()} # AÑADIDA EN UN 100%"

        codigo[linea] = comentario + ajuste

    def _obtener_ajuste_multilinea(self, mapeo_nodo: List[int]) -> str:
        """
        Obtiene texto de ajuste para cambios multilínea.

        Args:
            mapeo_nodo (List[int]): Lista de índices de líneas

        Returns:
            str: Texto de ajuste para el comentario

        Example:
            >>> _obtener_ajuste_multilinea([1, 2, 3])
            ' (las 3 líneas previas cuentan como 1)\n'
        """
        # Para cambios que afectan múltiples líneas, agregamos una nota
        # explicativa para clarificar que se cuentan como una sola modificación
        if len(mapeo_nodo) > 1:
            return f" (las {len(mapeo_nodo)} líneas previas cuentan como 1)\n"
        return "\n"
