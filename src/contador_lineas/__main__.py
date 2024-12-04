"""
Nombre del módulo: __main__.py
Ruta: contador_lineas/__main__.py
Descripción: Punto de entrada principal para el analizador de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 20-11-2024
Última Actualización: 20-11-2024

Dependencias:
    - argparse
    - colorama.Init, Fore, Style
    - pathlib.Path
    - core.contadores.analizador.AnalizadorCodigo, ExcepcionAnalizador
    - core.gestion_archivos.almacenamiento_metricas.AlmacenamientoMetricas
    - utils.formateador_metricas.mostrar_tabla_metricas

Uso:
    >>> contador_lineas archivo.py [-t] [-tc]
    
    Opciones:
        archivo.py: Ruta del archivo a analizar
        -t: Muestra tabla de LOC físicas y lógicas del archivo actual
        -tc: Muestra tabla de LOC físicas y lógicas de todos los archivos

Notas:
    - Requiere permisos de lectura en archivos a analizar
"""

import argparse
from pathlib import Path
from typing import Tuple

from colorama import init, Fore, Style

from contador_lineas.core.contadores.analizador import (
    AnalizadorCodigo, ExcepcionAnalizador
)
from contador_lineas.core.gestion_archivos.almacenamiento_metricas import (
    AlmacenamientoMetricas
)
from contador_lineas.utils.formateador_metricas import mostrar_tabla_metricas


def obtener_nombre_archivo(ruta_archivo: str) -> str:
    """
    Obtiene el nombre base de un archivo desde su ruta.

    Args:
        ruta_archivo (str): Ruta completa del archivo

    Returns:
        str: Nombre del archivo sin ruta

    Example:
        >>> obtener_nombre_archivo("c:/temp/archivo.py")
        'archivo.py'
    """
    return Path(ruta_archivo).name


def procesar_argumentos() -> argparse.Namespace:
    """
    Procesa los argumentos de línea de comandos.

    Returns:
        argparse.Namespace: Argumentos procesados

    Example:
        >>> args = procesar_argumentos()
        >>> print(args.ruta_archivo)
        'archivo.py'
    """
    analizador = argparse.ArgumentParser(
        description="Sistema de Conteo de Líneas Físicas y Lógicas en Python"
    )
    analizador.add_argument(
        "ruta_archivo",
        type=str,
        nargs='?',
        help="Ruta del archivo Python a analizar"
    )
    analizador.add_argument(
        "-t",
        action="store_true",
        help="Mostrar tabla de métricas del archivo procesado"
    )
    analizador.add_argument(
        "-tc",
        action="store_true",
        help="Mostrar tabla de métricas de todos los archivos procesados"
    )
    return analizador.parse_args()


def imprimir_resultados() -> None:
    """
    Imprime un mensaje de éxito al procesar un archivo
    """
    mensaje_exito = (
        "¡Archivo procesado exitosamente! "
        "Las métricas guardadas en almacenamiento."
    )
    print(f"{Fore.GREEN}{mensaje_exito}{Style.RESET_ALL}")


def validar_argumentos(args: argparse.Namespace) -> Tuple[bool, str]:
    """
    Valida los argumentos de línea de comandos

    Args:
        args (argparse.Namespace): Argumentos procesados

    Returns:
        Tuple[bool, str]: (es_valido, mensaje_error)

    Example:
        >>> args = argparse.Namespace(ruta_archivo="archivo.py", t=True, 
                                                                    tc=False)
        >>> es_valido, error = validar_argumentos(args)
        >>> print(es_valido, error)
        True, ""
    """
    if not args.tc and not args.ruta_archivo:
        return False, "Error: Se requiere el archivo cuando no se usa -tc"
    return True, ""


def procesar_archivo(
        ruta_archivo: str,
        almacen: AlmacenamientoMetricas,
        mostrar_tabla: bool) -> None:
    """
    Procesa un archivo individual y muestra resultados.

    Args:
        ruta_archivo (str): Ruta del archivo a procesar
        almacen (AlmacenamientoMetricas): Almacenamiento de métricas
        mostrar_tabla (bool): Mostrar tabla de métricas
        formatear (bool): Guardar archivo formateado

    Example:
        >>> procesar_archivo("archivo.py", AlmacenamientoMetricas(), True)
    """
    nombre_archivo = obtener_nombre_archivo(ruta_archivo)
    analizador = AnalizadorCodigo()
    resultado = analizador.analizar_archivo(ruta_archivo, nombre_archivo)

    if mostrar_tabla:
        mostrar_tabla_metricas([
            almacen.cargar_metricas(nombre_archivo)
        ])


def main() -> None:
    """
    Punto de entrada principal del sistema de conteo de LOCs de código Python

    Example:
        >>> main()
    """
    init()
    args = procesar_argumentos()
    almacen = AlmacenamientoMetricas()

    # Caso especial: si solo se pide tabla completa (-tc), mostramos todas las
    # métricas y terminamos
    if args.tc and not args.ruta_archivo:
        mostrar_tabla_metricas(almacen.obtener_todas_las_metricas())
        return

    # Validamos argumentos antes de cualquier procesamiento para fallar rápido
    # si hay errores
    es_valido, mensaje_error = validar_argumentos(args)
    if not es_valido:
        print(f"{Fore.RED}{mensaje_error}{Style.RESET_ALL}")
        return

    try:
        # Procesamos el archivo actual y opcionalmente mostramos la tabla
        # histórica si se solicitó
        procesar_archivo(args.ruta_archivo, almacen, args.t)
        if args.tc:
            mostrar_tabla_metricas(almacen.obtener_todas_las_metricas())
    except ExcepcionAnalizador as e:
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
