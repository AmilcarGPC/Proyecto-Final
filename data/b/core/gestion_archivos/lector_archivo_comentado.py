"""
Nombre del módulo: lector_archivo.py
Ruta: src/core/gestion_archivos/lector_archivo.py
Descripción: Maneja la lectura y validación de archivos Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 16-11-2024
Última Actualización: 17-11-2024

Dependencias:
    - pathlib
    - typing
    - utils.validador.validar_archivo_python

Uso:
    from core.gestion_archivos.lector_archivo import LectorArchivoPython
    lector = LectorArchivoPython("script.py")
    lineas, error = lector.leer_lineas()

Notas:
    - Maneja archivos de texto en formato Python
    - Implementa caché para optimizar lecturas múltiples
"""

from pathlib import Path
from typing import Union, Optional

from analizador_cambios.utils.validador import validar_archivo_python # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.87%
from analizador_cambios.utils.archivo_utils import leer_archivo_texto # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.87%


class LectorArchivoPython:
    """
    Maneja la lectura y validación de archivos Python.

    Lee y valida archivos fuente Python, proporcionando métodos para
    validación y lectura línea por línea con manejo de errores.

    Attributes:
        ruta_archivo (Path): Ruta al archivo Python a leer
        _contenido (Optional[list[str]]): Contenido en caché del archivo

    Methods:
        validar() -> tuple[bool, str]: Valida si es un archivo Python válido
        leer_lineas() -> tuple[list[str], Optional[str]]: Lee todas las líneas
        contenido() -> list[str]: Retorna contenido en caché o lo lee

    Example:
        >>> lector = LectorArchivoPython("ejemplo.py")
        >>> lineas, error = lector.leer_lineas()
        >>> print(len(lineas))
        42
    """
    
    def __init__(self, ruta_archivo: Union[str, Path]):
        self.ruta_archivo = Path(ruta_archivo)
        self._contenido: Optional[list[str]] = None
        
    def validar(self) -> tuple[bool, str]:
        """
        Valida si el archivo es un archivo Python válido.

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)

        Example:
            >>> es_valido, error = lector.validar()
        """
        return validar_archivo_python(self.ruta_archivo)
    
    def leer_lineas(self) -> tuple[list[str], Optional[str]]:
        """
        Lee todas las líneas del archivo Python.

        Returns:
            tuple[list[str], Optional[str]]: (lineas, mensaje_error)

        Example:
            >>> lineas, error = lector.leer_lineas()
            def main(), ""
        """
        es_valido, error = self.validar()
        if not es_valido:
            return [], error
        
        self._contenido, error = leer_archivo_texto(self.ruta_archivo)
        return self._contenido, error
