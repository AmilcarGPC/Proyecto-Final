"""
Nombre del módulo: formateador_linea.py
Ruta: analizador_cambios/utils/formateador_linea.py
Descripción: Formatea líneas de código Python para cumplir con límites de 
             longitud
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 29-11-2024
Última Actualización: 01-12-2024

Dependencias:
    - config.longitud_lineas.LONGITUD_MAXIMA_LINEA
    - core.analizadores.analizador_cadenas.AnalizadorCadenas

Uso:
    from analizador_cambios.utils.formateador_linea import FormateadorLinea
    formateador = FormateadorLinea()
    lineas = formateador.formatear_linea("linea_muy_larga..")

Notas:
    - Mantiene la indentación original de las líneas
    - Soporta imports, definiciones de funciones y asignaciones
"""

from typing import List, Tuple

from analizador_cambios.config.longitud_lineas import LONGITUD_MAXIMA_LINEA
from contador_lineas.core.analizadores.analizador_cadenas import (
    AnalizadorCadenas
)


class ExcepcionFormateo(Exception):
    """
    Excepción personalizada para errores en formateo.

    Se lanza cuando una línea no puede ser formateada correctamente.

    Example:
        >>> raise ExcepcionFormateo("Línea demasiado larga")
    """

    pass


class FormateadorLinea:
    """
    Formatea líneas de código Python para no exceder la longitud máxima.

    Methods:
        formatear_linea: Formatea una línea según su tipo
        _formatear_importacion: Formatea declaraciones import
        _formatear_definicion_funcion: Formatea definiciones de funciones
        _formatear_asignacion: Formatea asignaciones
        _formatear_generico: Formatea otros tipos de líneas

    Example:
        >>> formateador = FormateadorLinea()
        >>> formateador.formatear_linea("def funcion(param1, param2, param3):")
        ['def funcion( \\', '    param2, \\', '    param3):']
    """
    @staticmethod
    def formatear_linea(linea: str) -> List[str]:
        """
        Formatea una línea considerando comentarios.
        """
        codigo, comentario = \
        FormateadorLinea._extraer_codigo_y_comentario(linea)

        if len(linea) <= LONGITUD_MAXIMA_LINEA:
            return [linea]

        indentacion = len(codigo) - len(codigo.lstrip())
        indentacion_str = ' ' * indentacion

        if comentario and len(codigo) <= LONGITUD_MAXIMA_LINEA:
            formateado = [codigo]
            formateado.extend(FormateadorLinea._formatear_comentario(comentario,
            indentacion_str))
            return formateado

        if codigo.strip().startswith(('from ', 'import ')):
            formateado = FormateadorLinea._formatear_importacion(codigo,
                         indentacion_str)
        elif codigo.strip().startswith('def ') and '(' in codigo:
            formateado = FormateadorLinea._formatear_definicion_funcion(codigo,
                         indentacion_str)
        elif '=' in codigo:
            formateado = FormateadorLinea._formatear_asignacion(codigo,
                         indentacion_str)
        else:
            formateado = FormateadorLinea._formatear_generico(codigo,
                         indentacion_str)

        if comentario:
            formateado.extend(FormateadorLinea._formatear_comentario(comentario,
            indentacion_str))

        return formateado

    @staticmethod
    def _extraer_codigo_y_comentario(linea: str) -> Tuple[str, str]:
        """
        Separa código, comentario y posición del comentario.
        """
        pos_hash = AnalizadorCadenas.encontrar_sin_comillas(linea, '#', 0)
        if pos_hash == -1:
            return linea, ''
        return linea[:pos_hash].rstrip(), linea[pos_hash:]

    @staticmethod
    def _formatear_comentario(comentario: str, indentacion: str) -> List[str]:
        """
        Formatea comentarios que exceden la longitud máxima.
        
        Args:
            comentario: Texto del comentario (con o sin #)
            indentacion: Espacios de indentación
        
        Returns:
            List[str]: Lista de líneas formateadas
        """
        comentario = comentario[1:].strip()

        linea_completa = indentacion + '# ' + comentario
        if len(linea_completa) <= LONGITUD_MAXIMA_LINEA:
            return [linea_completa]

        palabras = comentario.split()
        linea_actual = indentacion + '# ' + palabras[0]
        formateado = []

        for palabra in palabras[1:]:
            if len(linea_actual + ' ' + palabra) <= LONGITUD_MAXIMA_LINEA:
                linea_actual += ' ' + palabra
            else:
                formateado.append(linea_actual)
                linea_actual = indentacion + '# ' + palabra

        formateado.append(linea_actual)
        return formateado

    @staticmethod
    def _formatear_importacion(linea: str, indentacion: str) -> List[str]:
        """
        Formatea declaración de importación con múltiples elementos.

        Args:
            linea (str): Línea de código con declaración de importación
            indentacion (str): Espacios de indentación

        Returns:
            List[str]: Lista de líneas formateadas

        Example:
            >>> _formatear_importacion("from app import (module1, module2, 
                                                                    module3)")
            ['from app import (, \\', '    module1, \\', '    module2, \\', 
            '    module3)']
        """
        if linea.strip().startswith('import '):
            elementos = [elem.strip() for elem in linea[6:].strip().split(',')]
            formateado = []
            linea_actual = 'import '

            for i, elemento in enumerate(elementos):
                if not elemento:
                    continue

                if len(linea_actual + ', ' + elemento) + 3 <= \
                    LONGITUD_MAXIMA_LINEA:
                    linea_actual += ((', ' if linea_actual != 'import '
                                      else '')
                                     + elemento)
                else:
                    formateado.append(linea_actual + ', \\')
                    linea_actual = indentacion + elemento

            if linea_actual:
                formateado.append(linea_actual)

            return formateado

        if '(' in linea and ')' in linea:
            parte_importacion = linea[:linea.index('(')]
            parte_elementos = linea[linea.index('(')+1:linea.rindex(')')
                                    ].strip()
        else:
            parte_importacion = linea[:linea.index('import') + 6]
            parte_elementos = linea[linea.index('import') + 6:].strip()

        elementos = [elem.strip() for elem in parte_elementos.split(',')]
        formateado = [f"{indentacion}{parte_importacion.strip()} ("]
        indentacion_elem = indentacion + ' ' * 4

        for i, elemento in enumerate(elementos):
            if not elemento:
                continue
            if i < len(elementos) - 1:
                formateado.append(f"{indentacion_elem}{elemento},")
            else:
                formateado.append(f"{indentacion_elem}{elemento}")

        formateado.append(f"{indentacion})")
        return formateado

    @staticmethod
    def _formatear_definicion_funcion(linea: str,
                                      indentacion: str) -> List[str]:
        """
        Formatea definición de función con parámetros.

        Args:
            linea (str): Línea de código con definición de función
            indentacion (str): Espacios de indentación

        Returns:
            List[str]: Lista de líneas formateadas

        Example:
            >>> _formatear_definicion_funcion("def funcion(param1, param2):")
            ['def funcion( \\', '        param1, \\', '        param2):']
        """
        parte_funcion = linea[:linea.index('(')]
        parte_parametros = linea[linea.index('('):].strip('():')
        params = [p.strip() for p in parte_parametros.split(',')]

        formateado = [f"{parte_funcion}("]
        indentacion_params = indentacion + ' ' * 8

        for i, parametro in enumerate(params):
            if i < len(params) - 1:
                formateado.append(f"{indentacion_params}{parametro.strip()},")
            elif not parametro.endswith('):') and not parametro.endswith(':'):
                formateado.append(f"{indentacion_params}{parametro.strip()}):")
            else:
                formateado.append(f"{indentacion_params}{parametro.strip()}")

        return formateado

    @staticmethod
    def _formatear_3asignacion(linea: str, indentacion: str) -> List[str]:
        """
        Formatea asignaciones con múltiples elementos.

        Args:
            linea (str): Línea de código con asignación
            indentacion (str): Espacios de indentación

        Returns:
            List[str]: Lista de líneas formateadas

        Example:
            >>> _formatear_asignacion("variable = funcion(param1, param2)")
            ['variable = funcion( \\', '    param1, \\', '    param2)']
        """
        izquierda, derecha = linea.split('=', 1)
        print(izquierda, derecha)
        if '(' in derecha and ')' in derecha and \
            AnalizadorCadenas.encontrar_sin_comillas(linea, ',', 0, True) != -1:
            nombre_funcion = derecha[:derecha.index('(')].strip()
            texto_args = derecha[
                derecha.index('(')+1:derecha.rindex(')')
            ].strip()
            resto = (
                derecha[derecha.rindex(')'):].strip()
                if derecha.rindex(')') < len(derecha) - 1
                else ''
            )
            argumentos = [arg.strip() for arg in texto_args.split(',')]

            formateado = [
                f"{indentacion}{izquierda.strip()} = {nombre_funcion}("
            ]
            indentacion_args = indentacion + ' ' * 4

            for i, argumento in enumerate(argumentos):
                if i < len(argumentos) - 1:
                    formateado.append(f"{indentacion_args}{argumento},")
                else:
                    formateado.append(f"{indentacion_args}{argumento}")

            formateado.append(f"{indentacion}{resto}")
            return formateado

        print()
        return FormateadorLinea._formatear_generico(linea, indentacion)

    @staticmethod
    def _formatear_asignacion(linea: str, indentacion: str) -> List[str]:
        """
        Formatea asignaciones con múltiples elementos.

        Args:
            linea (str): Línea de código con asignación
            indentacion (str): Espacios de indentación

        Returns:
            List[str]: Lista de líneas formateadas

        Example:
            >>> _formatear_asignacion("variable = funcion(param1, param2)")
            ['variable = funcion( \\', '    param1, \\', '    param2)']
        """
        # Lista de operadores de asignación compuesta y comparación
        operadores = ['+=', '-=', '*=', '/=', '%=', '**=', '>>=',
                      '<<=', '&=', '|=', '^=', '==', '=']

        # Encontrar el operador correcto
        operador_encontrado = None
        pos_operador = -1

        for op in operadores:
            pos = AnalizadorCadenas.encontrar_sin_comillas(linea, op, 0, True)
            if pos != -1:
                if pos_operador == -1 or pos < pos_operador:
                    pos_operador = pos
                    operador_encontrado = op

        # Si no encontramos operador de asignación, usar el formato genérico
        if pos_operador == -1:
            return FormateadorLinea._formatear_generico(linea, indentacion)

        # Si es un operador de comparación, usar el formato genérico
        if operador_encontrado == '==':
            return FormateadorLinea._formatear_generico(linea, indentacion)

        izquierda = linea[:pos_operador]
        derecha = linea[pos_operador + len(operador_encontrado):]

        if '(' in derecha and ')' in derecha and \
            AnalizadorCadenas.encontrar_sin_comillas(linea, ',', 0, True) != -1:
            nombre_funcion = derecha[:derecha.index('(')].strip()
            texto_args = derecha[
                derecha.index('(')+1:derecha.rindex(')')
            ].strip()
            resto = (
                derecha[derecha.rindex(')'):].strip()
                if derecha.rindex(')') < len(derecha) - 1
                else ''
            )
            argumentos = [arg.strip() for arg in texto_args.split(',')]

            formateado = [
                f"{indentacion}{izquierda.strip()} {operador_encontrado} " + 
                f"{nombre_funcion}("
            ]
            indentacion_args = indentacion + ' ' * 4

            for i, argumento in enumerate(argumentos):
                if i < len(argumentos) - 1:
                    formateado.append(f"{indentacion_args}{argumento},")
                else:
                    formateado.append(f"{indentacion_args}{argumento}")

            formateado.append(f"{indentacion}{resto}")
            return formateado

        return FormateadorLinea._formatear_generico(linea, indentacion)

    @staticmethod
    def _formatear_generico(linea: str, indentacion: str) -> List[str]:
        """
        Formateo genérico para líneas largas.

        Args:
            linea (str): Línea de código a formatear
            indentacion (str): Espacios de indentación

        Returns:
            List[str]: Lista de líneas formateadas

        Example:    
            >>> _formatear_generico("json.loads('{"key": "value"}')")
            ['json.loads( \\','{"key": "value"})']
        """
        palabras = linea.split()
        linea_actual = indentacion
        formateado = []

        for i, palabra in enumerate(palabras):
            if i == 0 and len(palabra) + len(indentacion) + 2 > \
                LONGITUD_MAXIMA_LINEA:
                error = f"La línea '{linea.strip()}' es muy larga para ser " + \
                "formateada."
                raise ExcepcionFormateo(f"Línea inválida: {error}")
            if len(linea_actual) + len(palabra) + 2 <= LONGITUD_MAXIMA_LINEA:
                linea_actual += ((' ' if linea_actual != indentacion else '')
                                 + palabra)
            else:
                formateado.append(linea_actual + ' \\')
                linea_actual = indentacion + palabra

        if linea_actual.strip():
            formateado.append(linea_actual)

        return formateado
