# formatters.py
from typing import List
from tabulate import tabulate
from colorama import init, Fore, Style
from contador_lineas.models.metricas import MetricasArchivo

class MetricasFormatter:
    def __init__(self):
        init()
        self.theme = {
            'header': Fore.WHITE + Style.BRIGHT,
            'filename': Fore.GREEN,
            'logical': Fore.CYAN,
            'physical': Fore.YELLOW,
            'reset': Style.RESET_ALL
        }

    def format_table(self, metricas: List[MetricasArchivo]) -> None:
        headers = [
            f"{self.theme['header']}PROGRAMA{self.theme['reset']}",
            f"{self.theme['header']}LOC Lógicas{self.theme['reset']}",
            f"{self.theme['header']}LOC Físicas{self.theme['reset']}"
        ]

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
        ]

        print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))

def display_metrics_table(metricas: List[MetricasArchivo]) -> None:
    formatter = MetricasFormatter()
    formatter.format_table(metricas)
