"""
Nombre del módulo: main.py
Ruta: src/main.py
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
    - utils.formatters.display_metrics_table

Uso:
    >>> python main.py archivo.py [-t] [-tc]
    
    Opciones:
        archivo.py: Ruta del archivo a analizar
        -t: Muestra tabla de LOC físicas y lógicas del archivo actual
        -tc: Muestra tabla de LOC físicas y lógicas de todos los archivos

Notas:
    - Requiere permisos de lectura en archivos a analizar
"""
import argparse
from colorama import init, Fore, Style
from pathlib import Path

from contador_lineas.core.contadores.analizador import AnalizadorCodigo, ExcepcionAnalizador
from contador_lineas.core.gestion_archivos.almacenamiento_metricas import (
    AlmacenamientoMetricas
)
from contador_lineas.utils.archivo_utils import escribir_python
from contador_lineas.utils.formatters import display_metrics_table


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
    analizador.add_argument(
        "--formato",
        action="store_true",
        help="Guardar versión formateada del archivo"
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


def validar_argumentos(args: argparse.Namespace) -> tuple[bool, str]:
    """
    Valida los argumentos de línea de comandos

    Args:
        args (argparse.Namespace): Argumentos procesados

    Returns:
        tuple[bool, str]: (es_valido, mensaje_error)

    Example:
        >>> args = argparse.Namespace(ruta_archivo="archivo.py", t=True, tc=False)
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
        mostrar_tabla: bool,
        formatear: bool = False) -> None:
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

    if formatear:
        ruta_base = Path(ruta_archivo)
        ruta_formateada = ruta_base.parent / f"{ruta_base.stem}_formateado{ruta_base.suffix}"
        error = escribir_python(ruta_formateada, analizador.codigo)
        if error:
            print(f"{Fore.RED}{error}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Archivo formateado guardado en: {ruta_formateada}{Style.RESET_ALL}")

    if mostrar_tabla:
        display_metrics_table([
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

    if args.tc and not args.ruta_archivo:   
        display_metrics_table(almacen.obtener_todas_las_metricas())
        return

    es_valido, mensaje_error = validar_argumentos(args)
    if not es_valido:
        print(f"{Fore.RED}{mensaje_error}{Style.RESET_ALL}")
        return

    try:
        procesar_archivo(args.ruta_archivo, almacen, args.t, args.formato)
        if args.tc:   
            display_metrics_table(almacen.obtener_todas_las_metricas())
    except ExcepcionAnalizador as e:
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()