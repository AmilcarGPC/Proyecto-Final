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
from typing import Optional # AGREGADA TOTALMENTE NUEVA


@dataclass
class MetricasClase: # AGREGADA TOTALMENTE NUEVA
    """ # AGREGADA TOTALMENTE NUEVA
    Almacena las métricas de análisis de una clase Python. # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
    Attributes: # AGREGADA TOTALMENTE NUEVA
        nombre_clase (str): Nombre de la clase analizada # AGREGADA TOTALMENTE NUEVA
        cantidad_metodos (int): Número de métodos en la clase # AGREGADA TOTALMENTE NUEVA
        lineas_fisicas (int): Número de líneas físicas en la clase # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
    Example: # AGREGADA TOTALMENTE NUEVA
        >>> metricas = MetricasClase("Clase", 10, 20) # AGREGADA TOTALMENTE NUEVA
    """ # AGREGADA TOTALMENTE NUEVA

    nombre_clase: str # AGREGADA TOTALMENTE NUEVA
    cantidad_metodos: int # AGREGADA TOTALMENTE NUEVA
    lineas_fisicas: int # AGREGADA TOTALMENTE NUEVA


@dataclass # AGREGADA TOTALMENTE NUEVA
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
    clases: list[MetricasClase] # AGREGADA TOTALMENTE NUEVA
    total_lineas_fisicas: Optional[int] = None # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.62%

    def __post_init__(self): # AGREGADA TOTALMENTE NUEVA
        self.total_lineas_fisicas = sum([clase.lineas_fisicas for clase in \
        self.clases]) # AGREGADA TOTALMENTE NUEVA (las 2 líneas previas cuentan como 1)
