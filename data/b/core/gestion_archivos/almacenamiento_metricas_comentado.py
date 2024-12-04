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
    from core.gestion_archivos.almacenamiento_metricas import (
        AlmacenamientoMetricas
    )
    
    almacen = AlmacenamientoMetricas()
    almacen.guardar_metricas(metricas)

Notas:
    - Almacena datos en formato JSON
    - Maneja errores de archivo no encontrado
"""

import os
from typing import List, Optional

from analizador_cambios.models.metricas import MetricasArchivo, MetricasClase # AÑADIDA EN UN 0.76%
from analizador_cambios.utils.archivo_utils import leer_json, escribir_json # AÑADIDA EN UN 0.88%


class AlmacenamientoMetricas:
    """
    Gestiona el almacenamiento persistente de métricas (Lineas Físicas y \
    Lógicas) en JSON.

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
    
    def __init__(
            self,
            ruta_almacenamiento: str = "db/lineas_por_clase_registro.json"): # AÑADIDA EN UN 0.88% (las 3 líneas previas cuentan como 1)
        self.ruta_almacenamiento = ruta_almacenamiento
        self._asegurar_archivo_almacenamiento()

    def guardar_metricas(self, metricas: MetricasArchivo) -> None:
        """
        Guarda nuevas métricas en el almacenamiento JSON.

        Args:
            metricas (MetricasArchivo): Métricas a almacenar
        """
        datos = leer_json(self.ruta_almacenamiento)
        
        # Convertir cada MetricasClase a diccionario # AÑADIDA EN UN 100%
        clases_dict = [
            {
                "nombre_clase": clase.nombre_clase,
                "cantidad_metodos": clase.cantidad_metodos,
                "lineas_fisicas": clase.lineas_fisicas
            } 
            for clase in metricas.clases
        ] # AÑADIDA EN UN 100% (las 8 líneas previas cuentan como 1)
        
        diccionario_metricas = {
            "nombre_archivo": metricas.nombre_archivo,
            "clases": clases_dict,
            "total_lineas_fisicas": metricas.total_lineas_fisicas
        } # AÑADIDA EN UN 0.83% (las 5 líneas previas cuentan como 1)
        
        datos[metricas.nombre_archivo] = diccionario_metricas
        escribir_json(self.ruta_almacenamiento, datos)

    def cargar_metricas(
            self,
            nombre_archivo: str) -> Optional[MetricasArchivo]:
        """
        Carga métricas almacenadas para un archivo.

        Args:
            nombre_archivo (str): Nombre del archivo a buscar

        Returns:
            Optional[MetricasArchivo]: Métricas encontradas o None
        """
        datos = leer_json(self.ruta_almacenamiento)
        if nombre_archivo in datos:
            diccionario_metricas = datos[nombre_archivo]
            
            # Reconstruir objetos MetricasClase # AÑADIDA EN UN 100%
            clases = [
                MetricasClase(**clase_dict)
                for clase_dict in diccionario_metricas["clases"]
            ] # AÑADIDA EN UN 100% (las 4 líneas previas cuentan como 1)
            
            # Crear MetricasArchivo con la lista de clases # AÑADIDA EN UN 0.61%
            return MetricasArchivo(
                nombre_archivo=diccionario_metricas["nombre_archivo"],
                clases=clases
            ) # AÑADIDA EN UN 100% (las 4 líneas previas cuentan como 1)
        return None

    def obtener_todas_las_metricas(self) -> List[MetricasArchivo]:
        """
        Obtiene lista de todas las métricas almacenadas.
        """
        datos = leer_json(self.ruta_almacenamiento)
        metricas = [] # AÑADIDA EN UN 100%
        
        for diccionario_metricas in datos.values(): # AÑADIDA EN UN 0.63%
            clases = [
                MetricasClase(**clase_dict)
                for clase_dict in diccionario_metricas["clases"]
            ] # AÑADIDA EN UN 100% (las 4 líneas previas cuentan como 1)
            metricas.append(MetricasArchivo(
                nombre_archivo=diccionario_metricas["nombre_archivo"],
                clases=clases
            )) # AÑADIDA EN UN 100% (las 4 líneas previas cuentan como 1)
        
        return metricas # AÑADIDA EN UN 100%

    def _asegurar_archivo_almacenamiento(self) -> None:
        """
        Crea el archivo JSON si no existe.

        Example:
            >>> _asegurar_archivo_almacenamiento()
        """
        if not os.path.exists(self.ruta_almacenamiento):
            escribir_json(self.ruta_almacenamiento, {})
