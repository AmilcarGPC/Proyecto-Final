"""
Nombre del módulo: validador.py
Ruta: contador_lineas/utils/validador.py
Descripción: Valida archivos Python y verifica su accesibilidad
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 19-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - pathlib.Path
    - typing.Union

Uso:
    from contador_lineas.utils.validador import validar_archivo_python
    es_valido, error = validar_archivo_python("script.py")
"""

from pathlib import Path
from typing import Union, Tuple


def validar_archivo_python(ruta_archivo: Union[str, Path]) -> Tuple[bool, str]:
    """
    Valida si una ruta corresponde a un archivo Python válido.

    Args:
        ruta_archivo (Union[str, Path]): Ruta del archivo a validar

    Returns:
        Tuple[bool, str]: (es_valido, mensaje_error)

    Raises:
        PermissionError: Si no hay permisos para leer el archivo
        OSError: Para otros errores del sistema de archivos

    Example:
        >>> es_valido, error = validar_archivo_python("script.py")
        >>> print(es_valido, error)
        True, ""
    """
    try:
        # Separamos la conversión y validación para mantener responsabilidades
        # únicas en cada función
        ruta = _convertir_a_ruta(ruta_archivo)
        return _validar_ruta(ruta)

    except PermissionError:
        return False, f"Permiso denegado al leer archivo: {ruta_archivo}"

    except Exception as error:
        return False, f"Error al acceder al archivo: {str(error)}"


def _convertir_a_ruta(ruta_archivo: Union[str, Path]) -> Path:
    """
    Convierte el parámetro de entrada a objeto Path.

    Args:
        ruta_archivo (Union[str, Path]): Ruta a convertir

    Returns:
        Path: Objeto Path creado
    """
    return Path(ruta_archivo)


def _validar_ruta(ruta: Path) -> Tuple[bool, str]:
    """
    Valida que la ruta exista y sea un archivo Python.

    Args:
        ruta (Path): Ruta a validar

    Returns:
        Tuple[bool, str]: (es_valido, mensaje_error)
    """
    if not ruta.exists():
        return False, f"El archivo '{ruta}' no fue encontrado"

    if not ruta.is_file():
        return False, f"La ruta '{ruta}' no es un archivo"

    if ruta.suffix.lower() != '.py':
        return False, f"El archivo '{ruta}' debe tener extensión .py"

    # Intentamos abrir y cerrar el archivo para verificar permisos de lectura
    # sin mantener el archivo abierto innecesariamente
    ruta.open('r').close()
    return True, ""
