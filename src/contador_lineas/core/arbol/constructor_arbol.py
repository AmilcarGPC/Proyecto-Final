"""
Nombre del módulo: constructor_arbol.py
Ruta: contador_lineas/core/arbol/constructor_arbol.py
Descripción: Construye un árbol sintáctico a partir de código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 19-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - typing.List
    - contador_lineas.core.analizadores.analizador_cadenas
    - contador_lineas.core.arbol.nodo
    - contador_lineas.models.nodos

Uso:
    from contador_lineas.core.arbol.constructor_arbol import ConstructorArbol
    constructor = ConstructorArbol()
    arbol = constructor.construir(lineas_codigo)
"""

from typing import List

from contador_lineas.core.analizadores.analizador_cadenas import (
    AnalizadorCadenas
)
from contador_lineas.core.arbol.analizador_nodos import AnalizadorTipoNodo
from contador_lineas.core.arbol.nodo import Nodo
from contador_lineas.config.node_types import PARENT_NODE_TYPES
from contador_lineas.models.nodos import TipoNodo


class ConstructorArbol:
    """
    Construye un árbol sintáctico a partir de código fuente Python.

    Procesa líneas de código y genera una estructura jerárquica que 
    representa la sintaxis del programa.

    Attributes:
        multilinea_vale_1 (bool): Indica si las líneas múltiples cuentan como 1
        analizador_tipo (AnalizadorTipoNodo): Analizador de tipos de nodos
        buffer_multilinea (List[str]): Buffer temporal para líneas múltiples
        delimitadores_abiertos (int): Contador de delimitadores sin cerrar
        en_cadena_multilinea (bool): Indica si está en cadena multilínea
        delimitador_cadena (str): Tipo de delimitador de cadena actual

    Methods:
        construir(lineas: List[str]) -> Nodo:
            Construye el árbol sintáctico a partir de las líneas de código

    Example:
        >>> constructor = ConstructorArbol()
        >>> arbol = constructor.construir(["def suma(a, b):", "  return a + b"])
    """

    def __init__(self, multilinea_vale_1: bool = True):
        self.multilinea_vale_1 = multilinea_vale_1
        self.analizador_tipo = AnalizadorTipoNodo()
        self.buffer_multilinea = []
        self.delimitadores_abiertos = 0
        self.en_cadena_multilinea = False
        self.delimitador_cadena = None

    def construir(self, lineas: List[str]) -> Nodo:
        """
        Construye el árbol sintáctico desde una lista de líneas.

        Args:
            lineas (List[str]): Lista de líneas de código a procesar

        Returns:
            Nodo: Raíz del árbol sintáctico construido

        Example:
            >>> construir(["def suma(a, b):", "    return a + b"])
        """
        raiz = Nodo(TipoNodo.ROOT, "raiz", -1)
        padre_actual = raiz
        # Usamos una pila para rastrear la indentación y los padres cada
        # elemento es una tupla (nodo_padre, nivel_indentacion)
        pila_indentacion = [(raiz, -1)]
        i = 0
        j = 0
        while i < len(lineas):
            linea = lineas[i]

            # Ignoramos líneas vacías para mantener la estructura limpia
            if not linea.strip():
                i += 1
                continue

            # Guardamos líneas múltiples en el buffer para procesarlas juntas
            if len(linea) > 1:
                self.buffer_multilinea = [l.strip() for l in linea]
            j = i

            # El orden de análisis es importante:
            # 1. Primero docstrings para evitar confusión con delimitadores
            # 2. Luego análisis de delimitadores para manejo de líneas múltiples
            # 3. Finalmente procesamiento normal de nodos
            if not self._analizar_docstring(linea):
                tipo_nodo = self.analizador_tipo.obtener_tipo_nodo(linea)
                indentacion = len(lineas[i]) - len(lineas[i].lstrip())
                nodo_nuevo = Nodo(tipo_nodo, lineas[i].strip(), indentacion)
                padre_actual.agregar_hijo(nodo_nuevo)

                # Procesamos líneas consecutivas del mismo tipo (útil para
                # docstrings y líneas múltiples)
                while i + 1 < len(lineas) and not self._analizar_docstring(
                lineas[i + 1]):
                    i += 1
                    indentacion = len(lineas[i]) - len(lineas[i].lstrip())
                    nodo_nuevo = Nodo(tipo_nodo, lineas[i].strip(), indentacion)
                    padre_actual.agregar_hijo(nodo_nuevo)

                if i + 1 < len(lineas):
                    i += 1

                linea = lineas[i]

            # Manejo especial para líneas múltiples con continuación (\)
            elif not self._analizar_delimitadores(linea.strip()):
                # Acumulamos líneas en el buffer hasta encontrar el final de la
                # expresión múltiple
                self.buffer_multilinea = [linea.strip()[:-1] if \
                linea.strip().endswith('\\') else linea.strip()]
                while i + 1 < len(lineas) and \
                not self._analizar_delimitadores(lineas[i + 1].strip()):
                    i += 1
                    self.buffer_multilinea.append(lineas[i].strip()[:-1] if \
                    lineas[i].strip().endswith('\\') else lineas[i].strip())

                if i + 1 < len(lineas):
                    i += 1
                    self.buffer_multilinea.append(lineas[i].strip())

                linea = ' '.join(self.buffer_multilinea)
                self.buffer_multilinea = []
                self.delimitadores_abiertos = 0

                tipo_nodo = self.analizador_tipo.obtener_tipo_nodo(linea)
            else:
                tipo_nodo = self.analizador_tipo.obtener_tipo_nodo(linea)

            indentacion = len(lineas[j]) - len(lineas[j].lstrip())
            nodo_nuevo = Nodo(tipo_nodo, linea.strip(), indentacion)

            # Ajustamos la jerarquía del árbol basándonos en la indentación
            # Subimos en la jerarquía mientras el nivel actual sea menor o igual
            # al nivel del tope de la pila
            while pila_indentacion and indentacion <= pila_indentacion[-1][1]:
                pila_indentacion.pop()
                if pila_indentacion:
                    padre_actual = pila_indentacion[-1][0]

            padre_actual.agregar_hijo(nodo_nuevo)

            # Si el nodo puede tener hijos, lo convertimos en el nuevo padre y
            # lo añadimos a la pila de indentación
            if self._puede_tener_hijos(tipo_nodo):
                padre_actual = nodo_nuevo
                pila_indentacion.append((nodo_nuevo, indentacion))

            i += 1

        return raiz

    def _es_asignacion_cadena(self, linea: str) -> bool:
        """
        Verifica si la línea contiene una asignación de cadena.

        Args:
            linea (str): Línea a verificar

        Returns:
            bool: True si es asignación de cadena

        Example:
            >>> _es_asignacion_cadena('x = "texto"')
            True
        """
        # Verificamos dos condiciones:
        # 1. Debe haber un operador de asignación
        # 2. El lado derecho debe contener delimitadores de cadena multilínea
        # Esto evita confundir asignaciones normales con asignaciones de cadenas
        linea_limpia = linea.strip()
        return ('=' in linea_limpia and
                ('"""' in linea_limpia.split('=')[1] or
                "'''" in linea_limpia.split('=')[1]))

    def _es_inicio_docstring_valido(self, linea: str) -> bool:
        """
        Verifica si la línea inicia un docstring válido.

        Args:
            linea (str): Línea a verificar

        Returns:
            bool: True si es inicio de docstring

        Example:
            >>> _es_inicio_docstring_valido('''Docstring''')
            True
        """
        # Solo consideramos docstrings que empiezan al inicio de la línea
        # (después de espacios) con comillas triples, ignorando docstrings que
        # aparezcan en medio de una línea
        linea_limpia = linea.strip()
        return (linea_limpia.startswith('"""') or
                linea_limpia.startswith("'''"))

    def _analizar_docstring(self, linea: str) -> bool:
        """
        Analiza si la línea está completa según reglas de docstring.

        Args:
            linea (str): Línea a analizar

        Returns:
            bool: True si la línea está completa

        Example:
            >>> _analizar_docstring('''Docstring''')
            True
        """
        linea_limpia = linea.strip()

        # Caso especial: asignación de cadena multilínea
        # Ejemplo: variable = """contenido"""
        if self._es_asignacion_cadena(linea_limpia):
            if not self.en_cadena_multilinea:
                # Buscamos delimitadores fuera de otras cadenas para evitar
                # falsos positivos en cadenas anidadas
                pos1 = AnalizadorCadenas.encontrar_sin_comillas(
                            linea_limpia,
                            '"""',
                            0
                        )
                pos2 = AnalizadorCadenas.encontrar_sin_comillas(
                            linea_limpia,
                            "'''",
                            0
                        )

                if pos1 == -1 and pos2 == -1:
                    return not self.en_cadena_multilinea

                # Si hay dos juegos de comillas triples en la misma línea, la
                # cadena está completa (ej: x = """texto""")
                contador_comillas = linea_limpia.count('"""') + \
                linea_limpia.count("'''")

                if contador_comillas == 2:
                    return True

                # Inicio de cadena multilínea, guardamos el tipo de delimitador
                # para asegurar que se cierre con el mismo tipo
                self.en_cadena_multilinea = True

                if pos1 != -1:
                    self.delimitador_cadena = '"""'
                else:
                    self.delimitador_cadena = "'''"
                return False
        # Caso: línea contiene comillas triples pero no es asignación
        elif '"""' in linea_limpia or "'''" in linea_limpia:
            pos1 = AnalizadorCadenas.encontrar_sin_comillas(
                        linea_limpia,
                        '"""',
                        0
                    )
            pos2 = AnalizadorCadenas.encontrar_sin_comillas(
                        linea_limpia,
                        "'''",
                        0
                    )

            if pos1 == -1 and pos2 == -1:
                return not self.en_cadena_multilinea

            # Caso: inicio de nuevo docstring (debe estar al inicio de línea)
            if not self.en_cadena_multilinea and \
            self._es_inicio_docstring_valido(linea_limpia):
                if pos1 != -1:
                    self.delimitador_cadena = '"""'
                else:
                    self.delimitador_cadena = "'''"

                # Docstring de una línea: abre y cierra en la misma línea
                if linea_limpia[3:].endswith(self.delimitador_cadena):
                    self.en_cadena_multilinea = False
                    self.delimitador_cadena = None
                    return True

                # Inicio de docstring multilínea
                self.en_cadena_multilinea = True
                return False

            # Caso: fin de docstring multilínea
            elif self.en_cadena_multilinea and self.delimitador_cadena in \
            linea_limpia:
                self.en_cadena_multilinea = False
                self.delimitador_cadena = None
                return True
            return False

        # Si no hay comillas triples, la línea está completa solo si
        # no estamos dentro de un docstring multilínea
        return not self.en_cadena_multilinea

    def _analizar_delimitadores(self, linea: str) -> bool:
        """
        Analiza si la línea está completa según delimitadores.

        Args:
            linea (str): Línea a analizar

        Returns:
            bool: True si los delimitadores están balanceados

        Example:
            >>> _analizar_delimitadores('def funcion():')
            True
        """
        # Buscamos cada tipo de delimitador fuera de cadenas de texto para
        # evitar falsos positivos con delimitadores en strings
        pos1 = AnalizadorCadenas.encontrar_sin_comillas(linea, '(', 0, True)
        pos2 = AnalizadorCadenas.encontrar_sin_comillas(linea, ")", 0, True)
        pos3 = AnalizadorCadenas.encontrar_sin_comillas(linea, '[', 0, True)
        pos4 = AnalizadorCadenas.encontrar_sin_comillas(linea, "]", 0, True)
        pos5 = AnalizadorCadenas.encontrar_sin_comillas(linea, '{', 0, True)
        pos6 = AnalizadorCadenas.encontrar_sin_comillas(linea, "}", 0, True)

        # Si no hay delimitadores, la línea está completa solo si:
        # 1. No hay delimitadores abiertos pendientes de líneas anteriores
        # 2. No termina en continuación explícita (\)
        if pos1 == -1 and pos2 == -1 and pos3 == -1 and pos4 == -1 and \
        pos5 == -1 and pos6 == -1:
            return self.delimitadores_abiertos == 0 and \
            not linea.rstrip().endswith('\\')

        if self.multilinea_vale_1:
            # Actualizamos el contador de delimitadores abiertos sumando
            # aperturas y restando cierres para mantener el balance en
            # expresiones multilínea
            self.delimitadores_abiertos += \
            (AnalizadorCadenas.contar_sin_comillas(linea, '(') +
                     AnalizadorCadenas.contar_sin_comillas(linea, '[') +
                     AnalizadorCadenas.contar_sin_comillas(linea, '{'))
            self.delimitadores_abiertos -= \
            (AnalizadorCadenas.contar_sin_comillas(linea, ')') +
                      AnalizadorCadenas.contar_sin_comillas(linea, ']') +
                      AnalizadorCadenas.contar_sin_comillas(linea, '}'))

        # La línea está completa solo si todos los delimitadores están
        # balanceados y no hay continuación explícita
        return self.delimitadores_abiertos == 0 and \
        not linea.rstrip().endswith('\\')

    def _puede_tener_hijos(self, tipo_nodo: TipoNodo) -> bool:
        """
        Verifica si un tipo de nodo puede contener nodos hijos.

        Args:
            tipo_nodo (TipoNodo): Tipo de nodo a verificar

        Returns:
            bool: True si puede tener hijos

        Example:
            >>> _puede_tener_hijos(TipoNodo.CLASS)
            True
        """
        return tipo_nodo in PARENT_NODE_TYPES
