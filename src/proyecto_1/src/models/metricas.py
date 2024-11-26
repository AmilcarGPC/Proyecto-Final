"""
Nombre del módulo: metricas.py
Ruta: src/models/metricas.py
Descripción: Define la estructura de datos para almacenar métricas 
             (Líneas Físicas y Lógicas) de archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 19/11/2024
Última Actualización: 19/11/2024

Dependencias:
    - dataclasses
    - datetime

Uso:
    from models.metricas import MetricasArchivo
    metricas = MetricasArchivo("archivo.py", 10, 20)

Notas:
    - La marca de tiempo se genera automáticamente si no se proporciona
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricasArchivo:
    """
    Almacena las métricas de análisis de un archivo Python.

    Attributes:
        nombre_archivo (str): Nombre del archivo analizado
        lineas_logicas (int): Número de líneas de código lógicas
        lineas_fisicas (int): Número de líneas físicas en el archivo
        marca_tiempo (str): Marca de tiempo ISO del análisis

    Example:
        >>> metricas = MetricasArchivo("test.py", 10, 20)
        >>> metricas.marca_tiempo is not None
        True
    """
    nombre_archivo: str
    lineas_logicas: int
    lineas_fisicas: int
    marca_tiempo: str = None
    
    def __post_init__(self) -> None:
        """
        Inicializa la marca de tiempo si no fue proporcionada.
        """
        if self.marca_tiempo is None:
            self.marca_tiempo = datetime.now().isoformat()