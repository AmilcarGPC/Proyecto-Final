# comparador_principal.py
from typing import List, Union
from analizador_cambios.models.cambios import Cambio, TipoCambio
from analizador_cambios.core.arbol.arbol_sintactico import ArbolArchivoPython
from analizador_cambios.core.arbol.comparador_arboles import ComparadorArboles


class ComparadorVersiones:
    def __init__(self):
        self.comparador = ComparadorArboles()    

    def comparar_archivos(self, arbol_v1: ArbolArchivoPython, arbol_v2: ArbolArchivoPython, espacios_blanco: bool = False) -> str:
        """
        Compara dos versiones de un archivo y genera un reporte de diferencias.
        
        Args:
            contenido_v1: Contenido del archivo original
            contenido_v2: Contenido del archivo modificado
            
        Returns:
            str: Reporte formateado de las diferencias
        """
        
        cambios = self.comparador.comparar(arbol_v1.raiz, arbol_v2.raiz, espacios_blanco)

        return cambios
    
    def contar_cambios(self, cambios: List[Cambio]) -> Union[int, int, int]:
        """
        Cuenta la cantidad de cambios en un reporte.
        
        Args:
            cambios: Reporte de cambios
            
        Returns:
            Tuple[int, int]: Cantidad de líneas agregadas, modificadas y borradas
        """
        cantidad_agregadas = 0
        cantidad_agregadas_modificadas = 0
        cantidad_borradas = 0

        for cambio in cambios:
            if cambio.tipo == TipoCambio.AGREGADA:
                if cambio.medida_de_cambio != 100:
                    cantidad_agregadas_modificadas += 1
                else:
                    cantidad_agregadas += 1
            elif cambio.tipo == TipoCambio.BORRADA:
                cantidad_borradas += 1

        return cantidad_agregadas, cantidad_agregadas_modificadas, cantidad_borradas