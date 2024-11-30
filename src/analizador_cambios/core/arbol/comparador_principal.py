# comparador_principal.py
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