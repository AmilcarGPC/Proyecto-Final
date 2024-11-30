# generador_reporte.py
from typing import List, Dict
from colorama import init, Fore, Style
from analizador_cambios.models.cambios import Cambio, TipoCambio

class GeneradorReporte:
    def __init__(self):
        init()  # Initialize colorama
    
    def generar_reporte(self, cambios: List[Cambio]) -> str:
        if not cambios:
            return "No se encontraron cambios"
        
        reporte = []
        for cambio in cambios:
            if cambio.tipo == TipoCambio.ELIMINADO:
                reporte.append(f"{Fore.RED}- {cambio.nodo_original.contenido}{Style.RESET_ALL}")
            elif cambio.tipo == TipoCambio.AGREGADO:
                reporte.append(f"{Fore.GREEN}+ {cambio.nodo_nuevo.contenido}{Style.RESET_ALL}")
            elif cambio.tipo == TipoCambio.MODIFICADO:
                reporte.append(f"{Fore.YELLOW}* {cambio.nodo_original.contenido} → {cambio.nodo_nuevo.contenido}{Style.RESET_ALL}")
            else:
                reporte.append(f" {cambio.nodo_original.contenido}")
        
        return "\n".join(reporte)