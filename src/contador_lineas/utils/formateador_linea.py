"""
Nombre del módulo: formateador_linea.py
Ruta: src/utils/formateador_linea.py
Descripción: Formatea líneas de código Python para cumplir con límites de longitud
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 19-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - config.longitud_lineas.LONGITUD_MAXIMA_LINEA

Uso:
    from utils.formateador_linea import FormateadorLinea
    formateador = FormateadorLinea()
    lineas = formateador.formatear_linea("linea_muy_larga...")

Notas:
    - Mantiene la indentación original de las líneas
    - Soporta imports, definiciones de funciones y asignaciones
"""

from contador_lineas.config.longitud_lineas import LONGITUD_MAXIMA_LINEA

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
    def formatear_linea(linea: str) -> list[str]:
        """
        Formatea una línea según su tipo y contenido.

        Args:
            linea (str): Línea de código a formatear

        Returns:
            list[str]: Lista de líneas formateadas

        Example:
            >>> formatear_linea("def funcion(param1, param2)")
            ['def funcion(', '        param1,', '        param2):']
        """
        indentacion = len(linea) - len(linea.lstrip())
        indentacion_str = ' ' * indentacion

        if linea.strip().startswith(('from ', 'import ')):
            return FormateadorLinea._formatear_importacion(
                linea, 
                indentacion_str
            )

        if len(linea) <= LONGITUD_MAXIMA_LINEA:
            return [linea]

        if linea.strip().startswith('def ') and '(' in linea:
            return FormateadorLinea._formatear_definicion_funcion(
                linea, 
                indentacion_str
            )

        if '=' in linea:
            return FormateadorLinea._formatear_asignacion(
                linea, 
                indentacion_str
            )

        return FormateadorLinea._formatear_generico(linea, indentacion_str)
    
    @staticmethod
    def _formatear_importacion(linea: str, indentacion: str) -> list[str]:
        """
        Formatea declaración de importación con múltiples elementos.

        Args:
            linea (str): Línea de código con declaración de importación
            indentacion (str): Espacios de indentación

        Returns:
            list[str]: Lista de líneas formateadas

        Example:
            >>> _formatear_importacion("from app import (module1, module2, module3)")
            ['from app import (, \\', '    module1, \\', '    module2, \\', '    module3)']
        """
        if linea.strip().startswith('import '):
            elementos = [elem.strip() for elem in linea[6:].strip().split(',')]
            formateado = []
            linea_actual = 'import '
            
            for i, elemento in enumerate(elementos):
                if not elemento:
                    continue

                if len(linea_actual + elemento) <= LONGITUD_MAXIMA_LINEA:
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
        formateado = [f"{parte_importacion.strip()} ("]
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
                                      indentacion: str) -> list[str]:
        """
        Formatea definición de función con parámetros.

        Args:
            linea (str): Línea de código con definición de función
            indentacion (str): Espacios de indentación

        Returns:
            list[str]: Lista de líneas formateadas

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
    def _formatear_asignacion(linea: str, indentacion: str) -> list[str]:
        """
        Formatea asignaciones con múltiples elementos.

        Args:
            linea (str): Línea de código con asignación
            indentacion (str): Espacios de indentación

        Returns:
            list[str]: Lista de líneas formateadas

        Example:
            >>> _formatear_asignacion("variable = funcion(param1, param2)")
            ['variable = funcion( \\', '    param1, \\', '    param2)']
        """
        izquierda, derecha = linea.split('=', 1)
        if '(' in derecha and ')' in derecha:
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

        return FormateadorLinea._formatear_generico(linea, indentacion)
    
    @staticmethod
    def _formatear_generico(linea: str, indentacion: str) -> list[str]:
        """
        Formateo genérico para líneas largas.

        Args:
            linea (str): Línea de código a formatear
            indentacion (str): Espacios de indentación

        Returns:
            list[str]: Lista de líneas formateadas

        Example:    
            >>> _formatear_generico("json.loads('{"key": "value"}')")
            ['json.loads( \\','{"key": "value"})']
        """
        palabras = linea.split()
        linea_actual = indentacion
        formateado = []

        for palabra in palabras:
            if len(linea_actual) + len(palabra) + 1 <= LONGITUD_MAXIMA_LINEA:
                linea_actual += ((' ' if linea_actual != indentacion else '') 
                                 + palabra)
            else:
                formateado.append(linea_actual + ' \\')
                linea_actual = indentacion + palabra

        if linea_actual.strip():
            formateado.append(linea_actual)

        return formateado