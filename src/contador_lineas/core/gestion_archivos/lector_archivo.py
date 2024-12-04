"""
Nombre del módulo: lector_archivo.py
Ruta: contador_lineas/core/gestion_archivos/lector_archivo.py
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
    from contador_lineas.core.gestion_archivos.lector_archivo import (
        LectorArchivoPython
    )
    lector = LectorArchivoPython("script.py")
    lineas, error = lector.leer_lineas()

Notas:
    - Maneja archivos de texto en formato Python
    - Implementa caché para optimizar lecturas múltiples
"""

from pathlib import Path
from typing import Union, Optional, List, Tuple

from contador_lineas.utils.validador import validar_archivo_python
from contador_lineas.utils.archivo_utils import leer_archivo_texto


class LectorArchivoPython:
    """
    Maneja la lectura y validación de archivos Python.

    Lee y valida archivos fuente Python, proporcionando métodos para
    validación y lectura línea por línea con manejo de errores.

    Attributes:
        ruta_archivo (Path): Ruta al archivo Python a leer
        _contenido (Optional[List[str]]): Contenido en caché del archivo

    Methods:
        validar() -> Tuple[bool, str]: Valida si es un archivo Python válido
        leer_lineas() -> Tuple[List[str], Optional[str]]: Lee todas las líneas
        contenido() -> List[str]: Retorna contenido en caché o lo lee

    Example:
        >>> lector = LectorArchivoPython("ejemplo.py")
        >>> lineas, error = lector.leer_lineas()
        >>> print(len(lineas))
        42
    """

    def __init__(self, ruta_archivo: Union[str, Path]):
        self.ruta_archivo = Path(ruta_archivo)
        self._contenido: Optional[List[str]] = None

    def validar(self) -> Tuple[bool, str]:
        """
        Valida si el archivo es un archivo Python válido.

        Returns:
            Tuple[bool, str]: (es_valido, mensaje_error)

        Example:
            >>> es_valido, error = lector.validar()
        """
        # Delegamos la validación a una función especializada para mantener la
        # separación de responsabilidades
        return validar_archivo_python(self.ruta_archivo)

    def leer_lineas(self) -> Tuple[List[str], Optional[str]]:
        """
        Lee todas las líneas del archivo Python.

        Returns:
            Tuple[List[str], Optional[str]]: (lineas, mensaje_error)

        Example:
            >>> lineas, error = lector.leer_lineas()
            def main(), ""
        """
        # Validamos primero para fallar rápido y evitar lecturas innecesarias de
        # archivos inválidos
        es_valido, error = self.validar()
        if not es_valido:
            return [], error

        # Guardamos el contenido en el objeto para permitir múltiples lecturas
        # sin acceder al almacenamiento cada vez
        self._contenido, error = leer_archivo_texto(self.ruta_archivo)
        return self._contenido, error
