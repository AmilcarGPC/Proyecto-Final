"""
Nombre del módulo: analizador_nodos.py
Ruta: contador_lineas/core/arbol/analizador_nodos.py
Descripción: Analiza y clasifica tipos de nodos en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - typing.Optional
    - contador_lineas.core.analizadores.analizador_cadenas.AnalizadorCadenas
    - contador_lineas.models.nodos.TipoNodo

Uso:
    from contador_lineas.core.arbol.analizador_nodos import (
        AnalizadorTipoNodo
    )
    analizador = AnalizadorTipoNodo()
    tipo = analizador.obtener_tipo_nodo(linea)
"""

from typing import Optional, List

from contador_lineas.core.analizadores.analizador_cadenas import (
    AnalizadorCadenas
)
from contador_lineas.models.nodos import TipoNodo


class AnalizadorTipoNodo:
    """
    Analiza y clasifica tipos de nodos en código Python.

    Procesa líneas de código y determina su tipo según su estructura
    y contenido sintáctico.

    Attributes:
        _en_clase (bool): Indica si está analizando una clase
        _es_nivel_modulo (bool): Indica si está en nivel de módulo
        _en_metodo (bool): Indica si está dentro de un método
        _clase_actual (str): Nombre de la clase actual en análisis

    Methods:
        obtener_tipo_nodo(linea: str) -> TipoNodo:
            Determina el tipo de nodo de una línea de código.
        ver_operaciones_especiales(linea: str) -> Optional[TipoNodo]:
            Verifica si la línea contiene operaciones especiales.
        verificar_comprensiones(linea: str) -> Optional[TipoNodo]:
            Verifica si la línea contiene comprensiones.

    Example:
        >>> analizador = AnalizadorTipoNodo()
        >>> analizador.obtener_tipo_nodo("def funcion():")
        TipoNodo.FUNCTION
    """
    def __init__(self):
        self._en_clase = False
        self._es_nivel_modulo = True
        self._en_metodo = False
        self._clase_actual = None

    def obtener_tipo_nodo(self, linea: str) -> TipoNodo:
        """
        Determina el tipo de nodo de una línea de código.

        Args:
            linea (str): Línea de código a analizar

        Returns:
            TipoNodo: Tipo de nodo identificado

        Example:
            >>> obtener_tipo_nodo("x = 5")
            TipoNodo.ASSIGNMENT
        """
        linea = linea.strip()

        if not linea:
            return TipoNodo.WHITE_SPACE

        # Se procesa async primero para normalizar la línea y reutilizar la
        # lógica existente
        prefijo_async = self._remover_prefijo_async(linea)
        if prefijo_async:
            return self.obtener_tipo_nodo(prefijo_async)

        tipo_docstring = self._obtener_tipo_docstring(linea)
        if tipo_docstring:
            return tipo_docstring

        if linea.startswith('#'):
            return TipoNodo.COMMENT

        tipo_constante_prop = self._verificar_constantes_e_imports(linea)
        if tipo_constante_prop:
            return tipo_constante_prop

        tipo_definicion = self._verificar_definiciones(linea)
        if tipo_definicion:
            return tipo_definicion

        tipo_flujo_control = self._verificar_condicionales(linea)
        if tipo_flujo_control:
            return tipo_flujo_control

        tipo_comprension = self.verificar_comprensiones(linea)
        if tipo_comprension:
            return tipo_comprension

        tipo_op_especial = self.ver_operaciones_especiales(linea)
        if tipo_op_especial:
            return tipo_op_especial

        tipo_sentencia_salto = self._verificar_sentencias_salto(linea)
        if tipo_sentencia_salto:
            return tipo_sentencia_salto

        tipo_decorador_import = self._verificar_decoradores_y_propiedades(linea)
        if tipo_decorador_import:
            return tipo_decorador_import

        # Verificación de asignación después de todas las reglas especiales para
        # evitar falsos positivos con operadores de comparación
        if '=' in linea:
            index = linea.index('=')
            pos1 = AnalizadorCadenas().encontrar_sin_comillas(linea, '(', 0,
                                                              True)
            pos2 = AnalizadorCadenas().encontrar_sin_comillas(linea, ')', 0,
                                                              True)
            # Ignora '=' si está dentro de paréntesis (ej: función con kwargs)
            if not (index > pos1 and index < pos2):
                return TipoNodo.ASSIGNMENT

        return TipoNodo.EXPRESSION

    def verificar_comprensiones(self, linea: str) -> Optional[TipoNodo]:
        """
        Verifica si la línea contiene una comprensión.

        Args:
            linea (str): Línea a verificar

        Returns:
            Optional[TipoNodo]: Tipo de comprensión o None

        Example:
            >>> verificar_comprensiones("[x for x in range(5)]")
            TipoNodo.LIST_COMPREHENSION
        """
        # Función anidada para evitar duplicación en la lógica de validación de
        # diferentes tipos de comprensiones (lista, dict, set, generator)
        def tiene_contenido_valido(
                inicio: int,
                fin: int,
                palabras_clave: List[str]) -> bool:
            if inicio >= fin:
                return False
            contenido = linea[inicio + 1:fin]
            return all(palabra in contenido for palabra in palabras_clave)

        if '[' in linea and ']' in linea:
            inicio = linea.index('[')
            fin = linea.rindex(']')
            if tiene_contenido_valido(inicio, fin, [' for ']):
                return TipoNodo.LIST_COMPREHENSION

        if '{' in linea and '}' in linea:
            inicio = linea.index('{')
            fin = linea.rindex('}')
            # La presencia de ':' distingue dict de set comprehension
            if tiene_contenido_valido(inicio, fin, [' : ', ' for ']):
                return TipoNodo.DICT_COMPREHENSION
            elif tiene_contenido_valido(inicio, fin, [' for ']):
                return TipoNodo.SET_COMPREHENSION

        if '(' in linea and ')' in linea:
            inicio = linea.index('(')
            fin = linea.rindex(')')
            if tiene_contenido_valido(inicio, fin, [' for ']):
                return TipoNodo.GENERATOR_EXPRESSION

        return None

    def ver_operaciones_especiales(self, linea: str) -> Optional[TipoNodo]:
        """
        Identifica operaciones especiales como with, try, etc.

        Args:
            linea (str): Línea a verificar

        Returns:
            Optional[TipoNodo]: Tipo de operación o None

        Example:
            >>> ver_operaciones_especiales("with open('file'):")
            TipoNodo.WITH
        """
        if linea.startswith('with '):
            return TipoNodo.WITH

        if linea.startswith('try:'):
            return TipoNodo.TRY

        if linea.startswith('except'):
            return TipoNodo.EXCEPT

        if linea.startswith('finally:'):
            return TipoNodo.FINALLY

        if ' if ' in linea and ' else ' in linea and \
        not linea.startswith('if '):
            return TipoNodo.TERNARY

        return None

    def _obtener_tipo_docstring(self, linea: str) -> TipoNodo:
        """
        Identifica si la línea es un docstring y su tipo.

        Args:
            linea (str): Línea a verificar

        Returns:
            TipoNodo: Tipo de docstring o None

        Example:
            >>> _obtener_tipo_docstring('''Docstring del módulo''')
            TipoNodo.MODULE_DOCSTRING
        """
        # El orden de verificación es importante:
        # 1. Nivel módulo (más externo)
        # 2. Dentro de clase
        # 3. Dentro de función/método (caso por defecto)
        if linea.startswith('"""') or linea.startswith("'''"):
            if self._es_nivel_modulo:
                return TipoNodo.MODULE_DOCSTRING
            elif self._en_clase:
                return TipoNodo.CLASS_DOCSTRING
            return TipoNodo.FUNCTION_DOCSTRING
        return None

    def _verificar_definiciones(self, linea: str) -> Optional[TipoNodo]:
        """
        Verifica si la línea define una clase, función o método.

        Args:
            linea (str): Línea a verificar

        Returns:
            Optional[TipoNodo]: Tipo de definición o None

        Example:
            >>> _verificar_definiciones('def funcion():')
            TipoNodo.FUNCTION
        """
        if linea.startswith('def '):
            # Reseteamos el flag de nivel módulo ya que entramos en un scope más
            # profundo
            self._es_nivel_modulo = False
            if self._en_clase:
                self._en_metodo = True
                return TipoNodo.METHOD
            return TipoNodo.FUNCTION

        # Actualizamos todos los estados al entrar en una clase para mantener
        # consistencia en el análisis de contexto
        if linea.startswith('class '):
            self._en_clase = True
            self._en_metodo = False
            self._clase_actual = linea
            return TipoNodo.CLASS
        return None

    def _verificar_condicionales(self, linea: str) -> Optional[TipoNodo]:
        """
        Verifica si la línea contiene estructuras de control.

        Args:
            linea (str): Línea a verificar

        Returns:
            Optional[TipoNodo]: Tipo de estructura o None

        Example:
            >>> _verificar_condicionales('if condicion:')
            TipoNodo.IF
        """
        mapa_flujo_control = {
            'if ': TipoNodo.IF,
            'elif ': TipoNodo.ELIF,
            'else:': TipoNodo.ELSE,
            'for ': TipoNodo.FOR,
            'while ': TipoNodo.WHILE,
            'match ': TipoNodo.MATCH,
            'case ': TipoNodo.CASE,
        }

        for inicio, tipo_nodo in mapa_flujo_control.items():
            if linea.startswith(inicio):
                return tipo_nodo

        return None

    def _verificar_sentencias_salto(self, linea: str) -> Optional[TipoNodo]:
        """
        Verifica si la línea contiene sentencias de salto.

        Args:
            linea (str): Línea a verificar

        Returns:
            Optional[TipoNodo]: Tipo de sentencia o None

        Example:
            >>> _verificar_sentencias_salto('return valor')
            TipoNodo.RETURN
        """
        if linea.startswith('return '):
            return TipoNodo.RETURN

        if linea.startswith('break'):
            return TipoNodo.BREAK

        if linea.startswith('continue'):
            return TipoNodo.CONTINUE

        if linea.startswith('raise '):
            return TipoNodo.RAISE

        if linea.startswith('assert '):
            return TipoNodo.ASSERT
        return None

    def _verificar_decoradores_y_propiedades(
            self,
            linea: str) -> Optional[TipoNodo]:
        """
        Verifica si la línea contiene decoradores o propiedades.

        Args:
            linea (str): Línea a verificar

        Returns:
            Optional[TipoNodo]: Tipo de decorador o None

        Example:
            >>> _verificar_decoradores_y_propiedades('@property')
            TipoNodo.PROPERTY
        """
        if '@property' in linea:
            return TipoNodo.PROPERTY

        if linea.startswith('@'):
            return TipoNodo.DECORATOR

        return None

    def _verificar_constantes_e_imports(self, linea: str) -> Optional[TipoNodo]:
        """
        Verifica si la línea define constantes o importaciones.

        Args:
            linea (str): Línea a verificar

        Returns:
            Optional[TipoNodo]: Tipo de constante/import o None

        Example:
            >>> _verificar_constantes_e_imports('CONSTANTE = 42')
            TipoNodo.CONSTANT
        """
        if linea.isupper() and '=' in linea:
            return TipoNodo.CONSTANT

        if linea.startswith('import ') or linea.startswith('from '):
            return TipoNodo.IMPORT

        return None

    def _remover_prefijo_async(self, linea: str) -> str:
        """
        Remueve el prefijo 'async' de una línea si existe.

        Args:
            linea (str): Línea a verificar

        Returns:
            str: Línea sin prefijo async o None

        Example:
            >>> _remover_prefijo_async('async def funcion():')
            'def funcion():'
        """
        # Separamos el manejo de 'async' para simplificar el análisis posterior
        if linea.startswith('async '):
            return linea[6:].strip()
        return None
