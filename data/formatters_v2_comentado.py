# formatters.py
from typing import List
from tabulate import tabulate
from colorama import init, Fore, Style
from analizador_cambios.models.metricas import MetricasArchivo # AÑADIDA EN UN 14%

class MetricasFormatter:
    def __init__(self):
        init()
        self.theme = {
            'header': Fore.WHITE + Style.BRIGHT,
            'filename': Fore.GREEN,
            'class_name': Fore.CYAN,
            'methods': Fore.YELLOW,
            'loc': Fore.MAGENTA,
            'total': Fore.RED,
            'reset': Style.RESET_ALL
        } # AÑADIDA EN UN 19% (las 9 líneas previas cuentan como 1)

    def format_table(self, metricas: List[MetricasArchivo]) -> None:
        headers = [
            f"{self.theme['header']}PROGRAMA{self.theme['reset']}",
            f"{self.theme['header']}CLASE{self.theme['reset']}",
            f"{self.theme['header']}TOTAL DE MÉTODOS{self.theme['reset']}",
            f"{self.theme['header']}LOC FÍSICAS POR \
            CLASE{self.theme['reset']}",
            f"{self.theme['header']}" + "TOTAL DE LOC FÍSICA DEL PROGRAMA" + \
            f"{self.theme['reset']}"
        ] # AÑADIDA EN UN 100% (las 9 líneas previas cuentan como 1)

        rows = [] # AÑADIDA EN UN 100%
        for m in metricas: # AÑADIDA EN UN 100%
            # Primera fila con el nombre del programa y primera clase # AÑADIDA EN UN 100%
            first_class = m.clases[0] if m.clases else None # AÑADIDA EN UN 100%
            rows.append([
                f"{self.theme['filename']}{m.nombre_archivo}"+\
                "{self.theme['reset']}",
                f"{self.theme['class_name']}{first_class.nombre_clase if 
                first_class else '-'}{self.theme['reset']}",
                f"{self.theme['methods']}{first_class.cantidad_metodos if 
                first_class else 0}{self.theme['reset']}",
                f"{self.theme['loc']}{first_class.lineas_fisicas if 
                first_class else 0}{self.theme['reset']}",
                ""  # El total irá en una fila separada
            ]) # AÑADIDA EN UN 100% (las 11 líneas previas cuentan como 1)
            
            # Filas para el resto de clases # AÑADIDA EN UN 100%
            for clase in m.clases[1:]: # AÑADIDA EN UN 100%
                rows.append([
                    "",
                    f"{self.theme['class_name']}{clase.nombre_clase}" + \
                    f"{self.theme['reset']}",
                    f"{self.theme['methods']}{clase.cantidad_metodos}" + \
                    f"{self.theme['reset']}",
                    f"{self.theme['loc']}{clase.lineas_fisicas}" + \
                    f"{self.theme['reset']}",
                    ""
                ]) # AÑADIDA EN UN 100% (las 10 líneas previas cuentan como 1)
            
            # Fila con el total de líneas físicas # AÑADIDA EN UN 100%
            rows.append([
                "",
                "",
                "",
                "",
                f"{self.theme['total']}{m.total_lineas_fisicas}" + \
                f"{self.theme['reset']}"
            ]) # AÑADIDA EN UN 100% (las 8 líneas previas cuentan como 1)

        print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))

def display_metrics_table(metricas: List[MetricasArchivo]) -> None:
    formatter = MetricasFormatter()
    formatter.format_table(metricas)
