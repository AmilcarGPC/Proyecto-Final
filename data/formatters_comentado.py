# formatters.py
from typing import List
from tabulate import tabulate
from colorama import init, Fore, Style
from contador_lineas.models.metricas import MetricasArchivo # ELIMINADA

class MetricasFormatter:
    def __init__(self):
        init()
        self.theme = {
            'header': Fore.WHITE + Style.BRIGHT,
            'filename': Fore.GREEN,
            'logical': Fore.CYAN,
            'physical': Fore.YELLOW,
            'reset': Style.RESET_ALL
        } # ELIMINADA (las 7 líneas previas cuentan como 1)

    def format_table(self, metricas: List[MetricasArchivo]) -> None:
        headers = [
            f"{self.theme['header']}PROGRAMA{self.theme['reset']}",
            f"{self.theme['header']}LOC Lógicas{self.theme['reset']}",
            f"{self.theme['header']}LOC Físicas{self.theme['reset']}"
        ] # ELIMINADA (las 5 líneas previas cuentan como 1)

        rows = [
            [
                f"{self.theme['filename' ]}"
                f"{m.nombre_archivo}{self.theme['reset']}",
                f"{self.theme['logical']}"
                f"{m.lineas_logicas}{self.theme['reset']}",
                f"{self.theme['physical']}"
                f"{m.lineas_fisicas}{self.theme['reset']}"
            ]
            for m in metricas
        ] # ELIMINADA (las 11 líneas previas cuentan como 1)

        print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))

def display_metrics_table(metricas: List[MetricasArchivo]) -> None:
    formatter = MetricasFormatter()
    formatter.format_table(metricas)
