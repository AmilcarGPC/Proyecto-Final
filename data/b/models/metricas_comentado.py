"""
Nombre del módulo: metricas.py
Ruta: src/models/metricas.py
Descripción: Define la estructura de datos para almacenar métricas 
             (Líneas Físicas y Lógicas) de archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 19-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - dataclasses

Uso:
    from models.metricas import MetricasArchivo
    metricas = MetricasArchivo("archivo.py", 10, 20)

Notas:
    - La marca de tiempo se genera automáticamente si no se proporciona
"""

from dataclasses import dataclass
from typing import Optional # AÑADIDA EN UN 100%


@dataclass
class MetricasClase: # AÑADIDA EN UN 100%
    """ # AÑADIDA EN UN 100%
    Almacena las métricas de análisis de una clase Python. # AÑADIDA EN UN 100%
 # AÑADIDA EN UN 100%
    Attributes: # AÑADIDA EN UN 100%
        nombre_clase (str): Nombre de la clase analizada # AÑADIDA EN UN 100%
        cantidad_metodos (int): Número de métodos en la clase # AÑADIDA EN UN 100%
        lineas_fisicas (int): Número de líneas físicas en la clase # AÑADIDA EN UN 100%
 # AÑADIDA EN UN 100%
    Example: # AÑADIDA EN UN 100%
        >>> metricas = MetricasClase("Clase", 10, 20) # AÑADIDA EN UN 100%
    """ # AÑADIDA EN UN 100%

    nombre_clase: str # AÑADIDA EN UN 100%
    cantidad_metodos: int # AÑADIDA EN UN 100%
    lineas_fisicas: int # AÑADIDA EN UN 100%


@dataclass # AÑADIDA EN UN 100%
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
    clases: list[MetricasClase] # AÑADIDA EN UN 100%
    total_lineas_fisicas: Optional[int] = None # AÑADIDA EN UN 0.62%

    def __post_init__(self): # AÑADIDA EN UN 100%
        self.total_lineas_fisicas = sum([clase.lineas_fisicas for clase in \
        self.clases]) # AÑADIDA EN UN 100% (las 2 líneas previas cuentan como 1)
