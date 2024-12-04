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

from contador_lineas.core.contadores.analizador import (
    AnalizadorCodigo,
    ExcepcionAnalizador
) # ELIMINADA (las 4 líneas previas cuentan como 1)
from contador_lineas.core.gestion_archivos.almacenamiento_metricas import (
    AlmacenamientoMetricas
) # ELIMINADA (las 3 líneas previas cuentan como 1)
from contador_lineas.utils.archivo_utils import escribir_python # ELIMINADA
from contador_lineas.utils.formatters import display_metrics_table # ELIMINADA


def obtener_nombre_archivo(ruta_archivo: str) -> str:
    '''Obtiene el nombre base de un archivo desde su ruta''' # ELIMINADA
    return Path(ruta_archivo).name # ELIMINADA


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
    ) # ELIMINADA (las 6 líneas previas cuentan como 1)
    analizador.add_argument(
        "-t",
        action="store_true",
        help="Mostrar tabla de métricas del archivo procesado"
    ) # ELIMINADA (las 5 líneas previas cuentan como 1)
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


def validar_argumentos(args: argparse.Namespace) -> tuple[bool, str]:
    """
    Valida los argumentos de línea de comandos

    Args:
        args (argparse.Namespace): Argumentos procesados

    Returns:
        tuple[bool, str]: (es_valido, mensaje_error)

    Example:
        >>> args = argparse.Namespace(
            ruta_archivo="archivo.py",
            t=True,
            tc=False
        )
        >>> es_valido, error = validar_argumentos(args)
        >>> print(es_valido, error)
        True, ""
    """
    if not args.tc and not args.ruta_archivo: # ELIMINADA
        return False, "Error: Se requiere el archivo cuando no se usa -tc" # ELIMINADA
    return True, ""


def procesar_archivo(
        ruta_archivo: str,
        almacen: AlmacenamientoMetricas,
        mostrar_tabla: bool,
        formatear: bool = False) -> None: # ELIMINADA (las 5 líneas previas cuentan como 1)
    """
    Procesa un archivo individual y muestra resultados. # ELIMINADA
 # ELIMINADA
    Args: # ELIMINADA
        ruta_archivo (str): Ruta del archivo a procesar # ELIMINADA
        almacen (AlmacenamientoMetricas): Almacenamiento de métricas # ELIMINADA
        mostrar_tabla (bool): Mostrar tabla de métricas # ELIMINADA
        formatear (bool): Guardar archivo formateado # ELIMINADA
 # ELIMINADA
    Example: # ELIMINADA
        >>> procesar_archivo("archivo.py", AlmacenamientoMetricas(), True) # ELIMINADA
    """
    nombre_archivo = obtener_nombre_archivo(ruta_archivo) # ELIMINADA
    analizador = AnalizadorCodigo() # ELIMINADA
    resultado = analizador.analizar_archivo(ruta_archivo, nombre_archivo) # ELIMINADA

    if formatear: # ELIMINADA
        ruta_base = Path(ruta_archivo) # ELIMINADA
        ruta_formateada = ruta_base.parent / \
        f"{ruta_base.stem}_formateado{ruta_base.suffix}" # ELIMINADA (las 2 líneas previas cuentan como 1)
        error = escribir_python(ruta_formateada, analizador.codigo) # ELIMINADA
        if error: # ELIMINADA
            print(f"{Fore.RED}{error}{Style.RESET_ALL}") # ELIMINADA
        else: # ELIMINADA
            print(f"{Fore.GREEN}Archivo formateado guardado en: \
            {ruta_formateada}{Style.RESET_ALL}") # ELIMINADA (las 2 líneas previas cuentan como 1)

    if mostrar_tabla:
        display_metrics_table([
            almacen.cargar_metricas(nombre_archivo)
        ]) # ELIMINADA (las 3 líneas previas cuentan como 1)


def main() -> None:
    """
    Punto de entrada principal del sistema de conteo de LOCs de código Python

    Example:
        >>> main()
    """
    init()
    args = procesar_argumentos()
    almacen = AlmacenamientoMetricas()

    if args.tc and not args.ruta_archivo: # ELIMINADA
        display_metrics_table(almacen.obtener_todas_las_metricas())
        return

    es_valido, mensaje_error = validar_argumentos(args) # ELIMINADA
    if not es_valido:
        print(f"{Fore.RED}{mensaje_error}{Style.RESET_ALL}")
        return

    try:
        procesar_archivo(args.ruta_archivo, almacen, args.t) # ELIMINADA
        if args.tc:
            display_metrics_table(almacen.obtener_todas_las_metricas())
    except ExcepcionAnalizador as e:
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
