"""
Nombre del módulo: formateador_metricas.py
Ruta: contador_lineas/utils/formateador_metricas.py
Descripción: Procesa y formatea métricas de código para su visualización en 
             tabla
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - typing.List
    - tabulate.tabulate
    - colorama.init, Fore, Style
    - contador_lineas.models.metricas.MetricasArchivo

Uso:
    from contador_lineas.utils.formateador_metricas import (
        mostrar_tabla_metricas
    )
    mostrar_tabla_metricas(lista_metricas)
"""

from typing import List

from tabulate import tabulate
from colorama import init, Fore, Style

from contador_lineas.models.metricas import MetricasArchivo


class FormateadorMetricas:
    """
    Formatea métricas de código para visualización en tabla coloreada.

    Procesa métricas de archivos y las presenta en formato tabular con
    colores distintivos para cada tipo de información.

    Attributes:
        tema (dict): Diccionario con configuración de colores para tabla

    Methods:
        formatear_tabla(metricas: List[MetricasArchivo]) -> None:
            Genera y muestra una tabla formateada con las métricas.
    
    Example:
        >>> formateador = FormateadorMetricas()
        >>> formateador.formatear_tabla([metrica1, metrica2])
    """

    def __init__(self):
        init()
        # Se optó por usar un diccionario de tema para centralizar los colores y
        # facilitar cambios futuros en el esquema de colores sin modificar la
        # lógica de formateo
        self.tema = {
            'encabezado': Fore.WHITE + Style.BRIGHT,
            'nombre_archivo': Fore.GREEN,
            'logicas': Fore.CYAN,
            'fisicas': Fore.YELLOW,
            'reiniciar': Style.RESET_ALL
        }

    def formatear_tabla(self, metricas: List[MetricasArchivo]) -> None:
        """
        Genera y muestra una tabla formateada con las métricas.

        Args:
            metricas (List[MetricasArchivo]): Lista de métricas a formatear

        Example:
            >>> formateador.formatear_tabla([metrica1, metrica2])
        """
        # Separamos los encabezados con el tema aplicado para mantener
        # consistencia visual incluso si la tabla está vacía
        encabezados = [
            f"{self.tema['encabezado']}PROGRAMA{self.tema['reiniciar']}",
            f"{self.tema['encabezado']}LOC Lógicas{self.tema['reiniciar']}",
            f"{self.tema['encabezado']}LOC Físicas{self.tema['reiniciar']}"
        ]

        filas = [
            self._formatear_fila(m) for m in metricas
        ]

        # Añadimos un salto de línea inicial para separar visualmente la tabla
        # del contenido anterior en la consola
        print("\n" + tabulate(filas, headers=encabezados, tablefmt="grid"))

    def _formatear_fila(self, metrica: MetricasArchivo) -> List[str]:
        """
        Formatea una fila individual de métricas con colores.

        Args:
            metrica (MetricasArchivo): Métrica a formatear

        Returns:
            List[str]: Lista con valores formateados y coloreados
        """
        return [
            f"{self.tema['nombre_archivo']}"
            f"{metrica.nombre_archivo}{self.tema['reiniciar']}",
            f"{self.tema['logicas']}"
            f"{metrica.lineas_logicas}{self.tema['reiniciar']}",
            f"{self.tema['fisicas']}"
            f"{metrica.lineas_fisicas}{self.tema['reiniciar']}"
        ]


def mostrar_tabla_metricas(metricas: List[MetricasArchivo]) -> None:
    """
    Crea un formateador y muestra la tabla de métricas.

    Args:
        metricas (List[MetricasArchivo]): Lista de métricas a mostrar

    Example:
        >>> mostrar_tabla_metricas([metrica1, metrica2])
    """
    formateador = FormateadorMetricas()
    formateador.formatear_tabla(metricas)
