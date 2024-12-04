"""
Nombre del módulo: formateador_metricas.py
Ruta: lineas_por_clase/utils/formateador_metricas.py
Descripción: Procesa y formatea métricas de código para su visualización en 
             tabla
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 27-11-2024
Última Actualización: 28-11-2024

Dependencias:
    - typing.List
    - tabulate.tabulate
    - colorama.init, Fore, Style
    - contador_lineas.models.metricas.MetricasArchivo

Uso:
    from lineas_por_clase.utils.formateador_metricas import (
        mostrar_tabla_metricas
    )
    mostrar_tabla_metricas(lista_metricas)
"""

from typing import List

from tabulate import tabulate
from colorama import init, Fore, Style

from lineas_por_clase.models.metricas import MetricasArchivo

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
        self.tema = {
            'encabezado': Fore.WHITE + Style.BRIGHT,
            'nombre_archivo': Fore.GREEN,
            'nombre_clase': Fore.CYAN,
            'metodos': Fore.YELLOW,
            'loc': Fore.MAGENTA,
            'total': Fore.RED,
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
            f"{self.tema['encabezado']}CLASE{self.tema['reiniciar']}",
            f"{self.tema['encabezado']}" + "TOTAL DE MÉTODOS" + \
            f"{self.tema['reiniciar']}",
            f"{self.tema['encabezado']}" + "LOC FÍSICAS POR CLASE" + \
            f"{self.tema['reiniciar']}",
            f"{self.tema['encabezado']}" + "TOTAL DE LOC FÍSICA DEL PROGRAMA"+ \
            f"{self.tema['reiniciar']}"
        ]

        filas = self._formatear_fila(metricas)

        print("\n" + tabulate(filas, headers=encabezados, tablefmt="grid"))

    def _formatear_fila(self, metricas: List[MetricasArchivo]) -> List[str]:
        """
        Formatea un conjunto de filas de métricas con colores.

        Args:
            metrica (MetricasArchivo): Métrica a formatear

        Returns:
            List[str]: Lista con valores formateados y coloreados
        """
        filas = []
        for m in metricas:
            # Primera fila con el nombre del programa y primera clase
            primera_clase = m.clases[0] if m.clases else None

            # Pre-format theme elements to reduce line length
            tema_arch = self.tema['nombre_archivo']
            tema_clase = self.tema['nombre_clase']
            tema_met = self.tema['metodos']
            tema_loc = self.tema['loc']
            tema_total = self.tema['total']
            tema_reset = self.tema['reiniciar']

            filas.append([
                f"{tema_arch}{m.nombre_archivo}{tema_reset}",
                (f"{tema_clase}"
                f"{primera_clase.nombre_clase if primera_clase else '-'}"
                f"{tema_reset}"),
                f"{tema_met}" +
                f"{primera_clase.cantidad_metodos if primera_clase else 0}"
                f"{tema_reset}",
                f"{tema_loc}" +
                f"{primera_clase.lineas_fisicas if primera_clase else 0}"
                f"{tema_reset}",
                ""  # El total irá en una fila separada
            ])

            # Filas para el resto de clases
            for clase in m.clases[1:]:
                filas.append([
                    "",
                    f"{tema_clase}{clase.nombre_clase}{tema_reset}",
                    f"{tema_met}{clase.cantidad_metodos}{tema_reset}",
                    f"{tema_loc}{clase.lineas_fisicas}{tema_reset}",
                    ""
                ])

            # Fila con el total de líneas físicas
            filas.append([
                "", "", "", "",
                f"{tema_total}{m.total_lineas_fisicas}{tema_reset}"
            ])

        return filas

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
