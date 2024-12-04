"""
Nombre del módulo: archivo_utils.py
Ruta: src/utils/archivo_utils.py
Descripción: Utilidades para operaciones con archivos
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 17-11-2024
Última Actualización: 17-11-2024

Dependencias:
    - json
    - pathlib.Path
    - typing.Union, List, Optional, Tuple

Uso:
    from utils.archivo_utils import leer_archivo_texto

    contenido, error = leer_archivo_texto("C:/ejemplo.txt")

Notas:
    - Los archivos deben estar en codificación UTF-8
"""

import json
from pathlib import Path
from typing import Union, List, Optional, Tuple


def leer_archivo_texto(
    ruta_archivo: Union[str, Path], 
    codificacion: str = 'utf-8') -> Tuple[List[str], Optional[str]]:
    """
    Lee el contenido de un archivo de texto.

    Args:
        ruta_archivo (Union[str, Path]): Ruta del archivo a leer
        codificacion (str): Codificación del archivo. Por defecto UTF-8

    Returns:
        Tuple[List[str], Optional[str]]: Tupla conteniendo:
            - List[str]: Líneas leídas del archivo
            - Optional[str]: Mensaje de error si falló, None si fue exitoso

    Example:
        >>> lineas, error = leer_archivo_texto("ejemplo.txt")
        >>> if error:
        ...     print(f"Error: {error}")
        ... else:
        ...     print(f"Leídas {len(lineas)} líneas")
    """
    try:
        with open(ruta_archivo, 'r', encoding=codificacion) as archivo:
            return archivo.readlines(), None
    except UnicodeDecodeError:
        return [], f"Error de codificación, codificación esperada: \
        {codificacion}"
    except Exception as e:
        return [], f"Error al leer el archivo: {str(e)}"


def leer_json(ruta_archivo: Union[str, Path]) -> dict:
    """
    Lee un archivo JSON y retorna su contenido.

    Args:
        ruta_archivo (Union[str, Path]): Ruta del archivo JSON a leer

    Returns:
        dict: Contenido del archivo JSON

    Example:
        >>> datos = leer_json("config.json")
        >>> print(datos["versión"])
    """
    with open(ruta_archivo, 'r') as archivo:
        return json.load(archivo)


def escribir_json(ruta_archivo: Union[str, Path], datos: dict) -> None:
    """
    Escribe datos en un archivo JSON.

    Args:
        ruta_archivo (Union[str, Path]): Ruta donde guardar el archivo
        datos (dict): Datos a escribir en formato JSON

    Example:
        >>> escribir_json("config.json", {"versión": "1.0"})
    """
    with open(ruta_archivo, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def escribir_python(
    ruta_archivo: Union[str, Path],
    lineas: List[str],
    codificacion: str = 'utf-8') -> Optional[str]:
    """
    Escribe líneas de código Python en un archivo.

    Args:
        ruta_archivo (Union[str, Path]): Ruta donde guardar el archivo
        lineas (List[str]): Lista de strings con el código Python
        codificacion (str): Codificación del archivo. Por defecto UTF-8

    Returns:
        Optional[str]: Mensaje de error si falló, None si fue exitoso

    Example:
        >>> codigo = ['def suma(a, b):\\n', '    return a + b\\n']
        >>> error = escribir_python("ejemplo.py", codigo)
        >>> if error:
        ...     print(f"Error: {error}")
    """ 
    try:
        with open(ruta_archivo, 'w', encoding=codificacion) as archivo:
            for i, linea in enumerate(lineas):
                if linea != '\n':
                    if linea.endswith('\n'):
                        archivo.write(linea)
                    else:
                        archivo.write(linea + '\n')  # Escribir la línea actual
                else:
                    archivo.write('\n')
        return None
    except Exception as e:
        return f"Error al escribir el archivo: {str(e)}"
