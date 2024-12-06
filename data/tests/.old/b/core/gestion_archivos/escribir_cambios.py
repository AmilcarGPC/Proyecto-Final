from typing import List

from analizador_cambios.core.contadores.analizador import AnalizadorCodigo
from analizador_cambios.models.cambios import TipoCambio
from analizador_cambios.models.cambios import Cambio

class EscribirCambios:
    @staticmethod
    def escribir(analisis_1: AnalizadorCodigo, analisis_2: AnalizadorCodigo, cambios: List[Cambio]):
        """
        Crea copias de los códigos originales con comentarios en las líneas modificadas.

        Args:
            codigo1 (List[str]): Líneas del archivo original
            codigo2 (List[str]): Líneas del archivo modificado
            cambios (List[Cambio]): Lista de cambios realizados
        """

        # Crear copia de los códigos originales
        codigo1 = analisis_1.codigo
        codigo2 = analisis_2.codigo
        mapeo1 = analisis_1.arbol.mapeo_lineas
        mapeo2 = analisis_2.arbol.mapeo_lineas

        # Crear comentarios en las líneas modificadas
        for cambio in cambios:
            if cambio.tipo == TipoCambio.BORRADA:
                    linea = mapeo1[cambio.posicion][-1]
                    ajuste = f" (las {len(mapeo1[cambio.posicion])} líneas previas cuentan como 1)\n" if len(mapeo1[cambio.posicion]) > 1 else f"\n"
                    codigo1[linea] = f"{codigo1[linea].rstrip()} # ELIMINADA" + ajuste
            elif cambio.tipo == TipoCambio.AGREGADA:
                    linea = mapeo2[cambio.posicion][-1]
                    ajuste = f" (las {len(mapeo2[cambio.posicion])} líneas previas cuentan como 1)\n" if len(mapeo2[cambio.posicion]) > 1 else f"\n"
                    if cambio.medida_de_cambio != 100:
                        codigo2[linea] = f"{codigo2[linea].rstrip()} # AGREGADA PEQUEÑA MODIFICACIÓN DEL {cambio.medida_de_cambio}%" + ajuste
                    else:
                        codigo2[linea] = f"{codigo2[linea].rstrip()} # AGREGADA TOTALMENTE NUEVA" + ajuste

        return codigo1, codigo2
    
    def _verificar_no_backslash(self, linea: str):
        """
        Verifica si una línea de código termina con un backslash.

        Args:
            linea (str): Línea de código a verificar

        Returns:
            bool: True si termina con backslash, False si no
        """
        return linea.rstrip().endswith("\\")