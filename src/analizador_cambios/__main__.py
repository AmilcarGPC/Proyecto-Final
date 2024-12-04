"""
Nombre del módulo: __main__.py
Ruta: analizador_cambios/__main__.py
Descripción: Punto de entrada principal para el analizador de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 28-11-2024
Última Actualización: 02-12-2024

Dependencias:
    - argparse
    - colorama.Init, Fore, Style
    - pathlib.Path
    - core.contadores.analizador.AnalizadorCodigo, ExcepcionAnalizador
    - core.gestion_archivos.almacenamiento_metricas.AlmacenamientoMetricas
    - utils.formatters.mostrar_tabla_metricas

Uso:
    >>> analizador_cambios archivo1.py archivo2.py [-t] [-tc] [-cc]
    
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

from analizador_cambios.core.arbol.comparador_principal import (
    ComparadorVersiones
)
from analizador_cambios.core.contadores.analizador import (
    AnalizadorCodigo, ExcepcionAnalizador
)
from analizador_cambios.core.gestion_archivos.escribir_cambios import (
    EscribirCambios
)
from contador_lineas.utils.archivo_utils import escribir_python
from lineas_por_clase.core.gestion_archivos.almacenamiento_metricas import (
    AlmacenamientoMetricas
)
from lineas_por_clase.utils.formateador_metricas import mostrar_tabla_metricas


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
        "ruta_archivo_1",
        type=str,
        nargs='?',
        help="Ruta del primer archivo Python a analizar"
    )
    analizador.add_argument(
        "ruta_archivo_2",
        type=str,
        nargs='?',
        help="Ruta del segundo archivo Python a analizar"
    )
    analizador.add_argument(
        "-t",
        action="store_true",
        help="Mostrar tabla de métricas de los archivos procesados"
    )
    analizador.add_argument(
        "-tc",
        action="store_true",
        help="Mostrar tabla de métricas de todos los archivos procesados"
    )
    analizador.add_argument(
        "-cc",
        action="store_true",
        help="Mostrar conteo de cambios entre archivos"
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
    if not args.tc:
        if not (args.ruta_archivo_1 and args.ruta_archivo_2):
            return False, "Error: Se requieren dos archivos cuando no se usa -tc"
    return True, ""


def procesar_archivos(
        ruta_archivo_1: str,
        ruta_archivo_2: str,
        almacen: AlmacenamientoMetricas,
        mostrar_tabla: bool,
        mostrar_cambios: bool) -> None:
    """
    Procesa dos archivos, los compara y guarda resultados
    """
    nombre_archivo_1 = obtener_nombre_archivo(ruta_archivo_1)
    nombre_archivo_2 = obtener_nombre_archivo(ruta_archivo_2)

    analizador1 = AnalizadorCodigo()
    analizador2 = AnalizadorCodigo()

    resultado1 = analizador1.analizar_archivo(ruta_archivo_1, nombre_archivo_1)
    resultado2 = analizador2.analizar_archivo(ruta_archivo_2, nombre_archivo_2)

    comparador = ComparadorVersiones()
    cambios = comparador.comparar_archivos(analizador1.arbol, analizador2.arbol)

    escritor = EscribirCambios()
    codigo_1, codigo_2 = escritor.escribir(analizador1, analizador2, cambios)

    ruta_1 = Path(ruta_archivo_1)
    ruta_2 = Path(ruta_archivo_2)

    ruta_comentada_1 = ruta_1.parent / f"{ruta_1.stem}_comentado{ruta_1.suffix}"
    ruta_comentada_2 = ruta_2.parent / f"{ruta_2.stem}_comentado{ruta_2.suffix}"

    escribir_python(ruta_comentada_1, codigo_1)
    escribir_python(ruta_comentada_2, codigo_2)

    if mostrar_tabla:
        mostrar_tabla_metricas([
            almacen.cargar_metricas(nombre_archivo_1),
            almacen.cargar_metricas(nombre_archivo_2)
        ])

    if mostrar_cambios:
        agregados, modificados, eliminados = comparador.contar_cambios(cambios)
        print("\nConteo de cambios:")
        print(f"{Fore.GREEN}Líneas añadidas nuevas: {agregados}")
        print(f"{Fore.YELLOW}Líneas añadidas modificadas: {modificados}")
        print(f"{Fore.RED}Líneas eliminadas: {eliminados}{Style.RESET_ALL}\n")


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
    if args.tc and not (args.ruta_archivo_1 or args.ruta_archivo_2):
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
        procesar_archivos(
            args.ruta_archivo_1,
            args.ruta_archivo_2,
            almacen,
            args.t,
            args.cc
        )
        if args.tc:
            mostrar_tabla_metricas(almacen.obtener_todas_las_metricas())
    except ExcepcionAnalizador as e:
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
