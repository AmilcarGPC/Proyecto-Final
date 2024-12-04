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

# mientras # AGREGADA TOTALMENTE NUEVA
from analizador_cambios.utils.impresion_arbol import imprimir_arbol # AGREGADA TOTALMENTE NUEVA

from analizador_cambios.core.contadores.analizador import (
    AnalizadorCodigo,
    ExcepcionAnalizador
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.91% (las 4 líneas previas cuentan como 1)
from analizador_cambios.core.gestion_archivos.almacenamiento_metricas import (
    AlmacenamientoMetricas
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.92% (las 3 líneas previas cuentan como 1)
from analizador_cambios.utils.archivo_utils import escribir_python # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.87%
from analizador_cambios.utils.formatters import display_metrics_table # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.87%

from analizador_cambios.core.arbol.comparador_principal import (
    ComparadorVersiones
) # AGREGADA TOTALMENTE NUEVA (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.gestion_archivos.escribir_cambios import (
    EscribirCambios
) # AGREGADA TOTALMENTE NUEVA (las 3 líneas previas cuentan como 1)

def obtener_nombre_archivo(ruta_archivo: str) -> str:
    """ # AGREGADA TOTALMENTE NUEVA
    Obtiene el nombre base de un archivo desde su ruta. # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.93%
 # AGREGADA TOTALMENTE NUEVA
    Args: # AGREGADA TOTALMENTE NUEVA
        ruta_archivo (str): Ruta completa del archivo # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
    Returns: # AGREGADA TOTALMENTE NUEVA
        str: Nombre del archivo sin ruta # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
    Example: # AGREGADA TOTALMENTE NUEVA
        >>> obtener_nombre_archivo("c:/temp/archivo.py") # AGREGADA TOTALMENTE NUEVA
        'archivo.py' # AGREGADA TOTALMENTE NUEVA
    """ # AGREGADA TOTALMENTE NUEVA
    return Path(ruta_archivo).name # AGREGADA TOTALMENTE NUEVA


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
    ) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.96% (las 6 líneas previas cuentan como 1)
    analizador.add_argument(
        "ruta_archivo_2",
        type=str,
        nargs='?',
        help="Ruta del segundo archivo Python a analizar"
    ) # AGREGADA TOTALMENTE NUEVA (las 6 líneas previas cuentan como 1)
    analizador.add_argument(
        "-t",
        action="store_true",
        help="Mostrar tabla de métricas de los archivos procesados"
    ) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.98% (las 5 líneas previas cuentan como 1)
    analizador.add_argument(
        "-tc",
        action="store_true",
        help="Mostrar tabla de métricas de todos los archivos procesados"
    )
    analizador.add_argument(
        "-cc",
        action="store_true", 
        help="Mostrar conteo de cambios entre archivos"
    ) # AGREGADA TOTALMENTE NUEVA (las 5 líneas previas cuentan como 1)
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
    if not args.tc: # AGREGADA TOTALMENTE NUEVA
        if not (args.ruta_archivo_1 and args.ruta_archivo_2): # AGREGADA TOTALMENTE NUEVA
            return False, "Error: Se requieren dos archivos cuando no se usa \
            -tc" # AGREGADA TOTALMENTE NUEVA (las 2 líneas previas cuentan como 1)
    return True, ""


def procesar_archivos(
        ruta_archivo_1: str,
        ruta_archivo_2: str,
        almacen: AlmacenamientoMetricas,
        mostrar_tabla: bool,
        mostrar_cambios: bool) -> None: # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.83% (las 6 líneas previas cuentan como 1)
    """
    Procesa dos archivos, los compara y guarda resultados # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.67%
    """
    nombre_archivo_1 = obtener_nombre_archivo(ruta_archivo_1) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.96%
    nombre_archivo_2 = obtener_nombre_archivo(ruta_archivo_2) # 30 # AGREGADA TOTALMENTE NUEVA
    
    analizador1 = AnalizadorCodigo() # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.98%
    analizador2 = AnalizadorCodigo() # AGREGADA TOTALMENTE NUEVA
    
    resultado1 = analizador1.analizar_archivo(ruta_archivo_1, nombre_archivo_1) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.96%
    resultado2 = analizador2.analizar_archivo(ruta_archivo_2, nombre_archivo_2) # AGREGADA TOTALMENTE NUEVA

    # Realizar comparación # AGREGADA TOTALMENTE NUEVA
    comparador = ComparadorVersiones() # AGREGADA TOTALMENTE NUEVA
    cambios = comparador.comparar_archivos(
        analizador1.arbol,
        analizador2.arbol
    ) # AGREGADA TOTALMENTE NUEVA (las 4 líneas previas cuentan como 1)
    
    # Escribir archivos comentados # AGREGADA TOTALMENTE NUEVA
    escritor = EscribirCambios() # AGREGADA TOTALMENTE NUEVA
    codigo_1, codigo_2 = escritor.escribir(analizador1, analizador2, cambios) # AGREGADA TOTALMENTE NUEVA
    
    ruta_1 = Path(ruta_archivo_1) # AGREGADA TOTALMENTE NUEVA
    ruta_2 = Path(ruta_archivo_2) # AGREGADA TOTALMENTE NUEVA
    
    ruta_comentada_1 = ruta_1.parent / \
    f"{ruta_1.stem}_comentado{ruta_1.suffix}" # AGREGADA TOTALMENTE NUEVA (las 2 líneas previas cuentan como 1)
    ruta_comentada_2 = ruta_2.parent / \
    f"{ruta_2.stem}_comentado{ruta_2.suffix}" # AGREGADA TOTALMENTE NUEVA (las 2 líneas previas cuentan como 1)
    
    escribir_python(ruta_comentada_1, codigo_1) # AGREGADA TOTALMENTE NUEVA
    escribir_python(ruta_comentada_2, codigo_2) # AGREGADA TOTALMENTE NUEVA

    if mostrar_tabla:
        display_metrics_table([
            almacen.cargar_metricas(nombre_archivo_1),
            almacen.cargar_metricas(nombre_archivo_2)
        ]) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.75% (las 4 líneas previas cuentan como 1)

    if mostrar_cambios: # AGREGADA TOTALMENTE NUEVA
        agregados, modificados, eliminados = comparador.contar_cambios(cambios) # AGREGADA TOTALMENTE NUEVA
        print(f"\nConteo de cambios:") # AGREGADA TOTALMENTE NUEVA
        print(f"{Fore.GREEN}Líneas añadidas nuevas: {agregados}") # AGREGADA TOTALMENTE NUEVA
        print(f"{Fore.YELLOW}Líneas añadidas modificadas: {modificados}") # AGREGADA TOTALMENTE NUEVA
        print(f"{Fore.RED}Líneas eliminadas: {eliminados}{Style.RESET_ALL}\n") # AGREGADA TOTALMENTE NUEVA

def main() -> None:
    """
    Punto de entrada principal del sistema de conteo de LOCs de código Python

    Example:
        >>> main()
    """
    init()
    args = procesar_argumentos()
    almacen = AlmacenamientoMetricas()

    if args.tc and not (args.ruta_archivo_1 or args.ruta_archivo_2): # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.73%
        display_metrics_table(almacen.obtener_todas_las_metricas())
        return

    es_valido, mensaje_error = validar_argumentos(args) #60 # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.96%
    if not es_valido:
        print(f"{Fore.RED}{mensaje_error}{Style.RESET_ALL}")
        return

    try:
        procesar_archivos(
            args.ruta_archivo_1, 
            args.ruta_archivo_2, 
            almacen, 
            args.t,
            args.cc
        ) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.75% (las 7 líneas previas cuentan como 1)
        if args.tc:
            display_metrics_table(almacen.obtener_todas_las_metricas())
    except ExcepcionAnalizador as e:
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
