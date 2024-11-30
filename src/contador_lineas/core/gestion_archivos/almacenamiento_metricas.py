"""
Nombre del módulo: almacenamiento_metricas.py
Ruta: src/core/gestion_archivos/almacenamiento_metricas.py
Descripción: Gestiona el almacenamiento de métricas de archivos Python en JSON
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - os
    - typing.List, Optional
    - models.metricas.MetricasArchivo
    - utils.utilidades_archivo.leer_json, escribir_json

Uso:
    from core.gestion_archivos.almacenamiento_metricas import AlmacenamientoMetricas
    
    almacen = AlmacenamientoMetricas()
    almacen.guardar_metricas(metricas)

Notas:
    - Almacena datos en formato JSON
    - Maneja errores de archivo no encontrado
"""

import os
from typing import List, Optional

from contador_lineas.models.metricas import MetricasArchivo
from contador_lineas.utils.archivo_utils import leer_json, escribir_json


class AlmacenamientoMetricas:
    """
    Gestiona el almacenamiento persistente de métricas (Lineas Físicas y Lógicas) en JSON.

    Permite guardar y recuperar métricas de archivos Python,
    manteniendo un registro histórico en formato JSON.

    Attributes:
        ruta_almacenamiento (str): Ruta al archivo JSON de almacenamiento

    Methods:
        guardar_metricas(metricas: MetricasArchivo) -> None:
            Guarda nuevas métricas en el almacenamiento.
        cargar_metricas(nombre_archivo: str) -> Optional[MetricasArchivo]:
            Carga métricas para un archivo específico.
        obtener_todas_metricas() -> List[MetricasArchivo]:
            Obtiene todas las métricas almacenadas.

    Example:
        >>> almacen = AlmacenamientoMetricas("metricas.json")
        >>> almacen.guardar_metricas(metricas)
    """
    
    def __init__(self, ruta_almacenamiento: str = "db/contador_lineas_registro.json"):
        self.ruta_almacenamiento = ruta_almacenamiento
        self._asegurar_archivo_almacenamiento()

    def guardar_metricas(self, metricas: MetricasArchivo) -> None:
        """
        Guarda nuevas métricas en el almacenamiento JSON.

        Args:
            metricas (MetricasArchivo): Métricas a almacenar

        Example:
            >>> guardar_metricas(metricas_archivo)
        """
        datos = leer_json(self.ruta_almacenamiento)
        
        diccionario_metricas = {
            "nombre_archivo": metricas.nombre_archivo,
            "lineas_logicas": metricas.lineas_logicas,
            "lineas_fisicas": metricas.lineas_fisicas
        }
        
        datos[metricas.nombre_archivo] = diccionario_metricas
        escribir_json(self.ruta_almacenamiento, datos)

    def cargar_metricas(self, nombre_archivo: str) -> Optional[MetricasArchivo]:
        """
        Carga métricas almacenadas para un archivo.

        Args:
            nombre_archivo (str): Nombre del archivo a buscar

        Returns:
            Optional[MetricasArchivo]: Métricas encontradas o None

        Example:
            >>> cargar_metricas("script.py")
        """
        datos = leer_json(self.ruta_almacenamiento)
        if nombre_archivo in datos:
            diccionario_metricas = datos[nombre_archivo]
            return MetricasArchivo(**diccionario_metricas)
        return None

    def obtener_todas_las_metricas(self) -> List[MetricasArchivo]:
        """
        Obtiene lista de todas las métricas almacenadas.

        Returns:
            List[MetricasArchivo]: Lista de métricas encontradas

        Example:
            >>> obtener_todas_metricas()
        """
        datos = leer_json(self.ruta_almacenamiento)
        return [MetricasArchivo(**diccionario_metricas) 
                for diccionario_metricas in datos.values()]

    def _asegurar_archivo_almacenamiento(self) -> None:
        """
        Crea el archivo JSON si no existe.

        Example:
            >>> _asegurar_archivo_almacenamiento()
        """
        if not os.path.exists(self.ruta_almacenamiento):
            escribir_json(self.ruta_almacenamiento, {})