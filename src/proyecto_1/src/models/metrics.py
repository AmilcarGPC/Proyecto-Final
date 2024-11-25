# models/file_metrics.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MetricasArchivo:
    nombre_archivo: str
    lineas_logicas: int
    lineas_fisicas: int
    marca_tiempo: str = None
    
    def __post_init__(self):
        if self.marca_tiempo is None:
            self.marca_tiempo = datetime.now().isoformat()