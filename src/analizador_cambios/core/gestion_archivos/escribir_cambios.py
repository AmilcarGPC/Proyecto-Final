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
            if cambio.tipo == TipoCambio.MODIFICADO:
                for linea in mapeo2[cambio.posicion]:
                    codigo1[linea] = f"{codigo1[linea].rstrip('\n')} # ELIMINADO\n"
                    codigo2[linea] = f"{codigo2[linea].rstrip("\n")} # MODIFICADOA (PARCIALMENTE NUEVA)\n"
            elif cambio.tipo == TipoCambio.ELIMINADO:
                print(f"Eliminado: {cambio.posicion}")
                print(f"mapeo1: {mapeo1[cambio.posicion]}")
                for linea in mapeo1[cambio.posicion]:
                    print(f"a eliminar: {linea}")
                    codigo1[linea] = f"{codigo1[linea].rstrip("\n")} # ELIMINADO\n"
            elif cambio.tipo == TipoCambio.AGREGADO:
                for linea in mapeo2[cambio.posicion]:
                    print(f"a añadir: {linea}")
                    codigo2[linea] = f"{codigo2[linea].rstrip("\n")} # AGREGADO (TOTALMENTE NUEVA)\n"

        return codigo1, codigo2