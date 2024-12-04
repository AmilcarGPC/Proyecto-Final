"""
Nombre del módulo: metricas.py
Ruta: lineas_por_clase/models/metricas.py
Descripción: Define la estructura de datos para almacenar métricas 
             (Líneas Físicas y Lógicas) de archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 27-11-2024
Última Actualización: 28-11-2024

Dependencias:
    - dataclasses

Uso:
    from lineas_por_clase.models.metricas import MetricasArchivo
    metricas = MetricasArchivo("archivo.py", 10, 20)

Notas:
    - La marca de tiempo se genera automáticamente si no se proporciona
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class MetricasClase:
    """
    Almacena las métricas de análisis de una clase Python.

    Attributes:
        nombre_clase (str): Nombre de la clase analizada
        cantidad_metodos (int): Número de métodos en la clase
        lineas_fisicas (int): Número de líneas físicas en la clase

    Example:
        >>> metricas = MetricasClase("Clase", 10, 20)
    """

    nombre_clase: str
    cantidad_metodos: int
    lineas_fisicas: int


@dataclass
class MetricasArchivo:
    """
    Almacena las métricas de análisis de un archivo Python.

    Attributes:
        nombre_archivo (str): Nombre del archivo analizado
        lineas_logicas (int): Número de líneas de código lógicas
        lineas_fisicas (int): Número de líneas físicas en el archivo

    Example:
        >>> metricas = MetricasArchivo("test.py", 10, 20)
    """

    nombre_archivo: str
    clases: List[MetricasClase]
    total_lineas_fisicas: Optional[int] = None

    def __post_init__(self):
        self.total_lineas_fisicas = \
        sum([clase.lineas_fisicas for clase in self.clases])
