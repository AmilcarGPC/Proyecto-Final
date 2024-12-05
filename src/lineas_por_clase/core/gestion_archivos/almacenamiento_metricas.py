"""
Nombre del módulo: almacenamiento_metricas.py
Ruta: lineas_por_clase/core/gestion_archivos/almacenamiento_metricas.py
Descripción: Gestiona el almacenamiento de métricas de archivos Python en JSON
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 27-11-2024
Última Actualización: 28-11-2024

Dependencias:
    - os
    - typing.List, Optional
    - models.metricas.MetricasArchivo
    - utils.utilidades_archivo.leer_json, escribir_json

Uso:
    from lineas_por_clase.core.gestion_archivos.almacenamiento_metricas import (
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

from lineas_por_clase.models.metricas import MetricasArchivo, MetricasClase
from contador_lineas.utils.archivo_utils import leer_json, escribir_json


class AlmacenamientoMetricas:
    """
    Gestiona el almacenamiento persistente de métricas (Lineas Físicas y 
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
            ruta_almacenamiento: str):
        # Usamos un archivo JSON por defecto en la carpeta db/ para mantener
        # persistencia entre ejecuciones
        self.ruta_almacenamiento = ruta_almacenamiento
        self._asegurar_archivo_almacenamiento()

    def guardar_metricas(self, metricas: MetricasArchivo) -> None:
        """
        Guarda nuevas métricas en el almacenamiento JSON.

        Args:
            metricas (MetricasArchivo): Métricas a almacenar
        """
        datos = leer_json(self.ruta_almacenamiento)

        # Convertir cada MetricasClase a diccionario
        clases_dict = [
            {
                "nombre_clase": clase.nombre_clase,
                "cantidad_metodos": clase.cantidad_metodos,
                "lineas_fisicas": clase.lineas_fisicas
            }
            for clase in metricas.clases
        ]

        # Convertimos el objeto MetricasArchivo a diccionario para facilitar la
        # serialización JSON y mantener la estructura de datos consistente
        diccionario_metricas = {
            "nombre_archivo": metricas.nombre_archivo,
            "clases": clases_dict,
            "total_lineas_fisicas": metricas.total_lineas_fisicas
        }

        # Usamos el nombre del archivo como clave para permitir actualizaciones
        datos[metricas.nombre_archivo] = diccionario_metricas
        escribir_json(self.ruta_almacenamiento, datos)

    def cargar_metricas(self, nombre_archivo: str) -> Optional[MetricasArchivo]:
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

            # Reconstruir objetos MetricasClase
            clases = [
                MetricasClase(**clase_dict)
                for clase_dict in diccionario_metricas["clases"]
            ]

            # Crear MetricasArchivo con la lista de clases
            return MetricasArchivo(
                nombre_archivo=diccionario_metricas["nombre_archivo"],
                clases=clases
            )
        return None

    def obtener_todas_las_metricas(self) -> List[MetricasArchivo]:
        """
        Obtiene lista de todas las métricas almacenadas.
        """
        datos = leer_json(self.ruta_almacenamiento)
        metricas = []

        for diccionario_metricas in datos.values():
            clases = [
                MetricasClase(**clase_dict)
                for clase_dict in diccionario_metricas["clases"]
            ]
            metricas.append(MetricasArchivo(
                nombre_archivo=diccionario_metricas["nombre_archivo"],
                clases=clases
            ))

        return metricas

    def _asegurar_archivo_almacenamiento(self) -> None:
        """
        Crea el archivo JSON si no existe.

        Example:
            >>> _asegurar_archivo_almacenamiento()
        """
        # Inicializamos con un diccionario vacío para mantener una estructura
        # consistente desde el inicio
        if not os.path.exists(self.ruta_almacenamiento):
            escribir_json(self.ruta_almacenamiento, {})
