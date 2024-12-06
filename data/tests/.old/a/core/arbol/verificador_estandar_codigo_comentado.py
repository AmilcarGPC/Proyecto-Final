"""
Nombre del módulo: verificador_estandar_codigo.py
Ruta: src/core/arbol/verificador_estandar_codigo.py
Descripción: Verifica el cumplimiento de estándares de código Python en árboles \
sintácticos
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - core.analizadores.analizador_cadenas.AnalizadorCadenas
    - core.analizadores.analizador_expresiones.AnalizadorExpresiones
    - core.arbol.nodo.Nodo
    - config.node_types.PARENT_NODE_TYPES, COMMENT_NODE_TYPES, \
    NO_NESTED_ALLOWED
    - models.nodos.TipoNodo

Uso:
    from core.arbol.verificador_estandar_codigo import (
        VerificadorEstandarCodigo
    )

    verificador = VerificadorEstandarCodigo()
    es_valido, mensaje = verificador.es_arbol_sintactico_valido(raiz)

Notas:
    - Se basa en el estándar de código definido en el proyecto
"""

from contador_lineas.core.analizadores.analizador_cadenas import (
    AnalizadorCadenas
) # BORRADA (las 3 líneas previas cuentan como 1)
from contador_lineas.core.analizadores.analizador_expresiones import (
    AnalizadorExpresiones
) # BORRADA (las 3 líneas previas cuentan como 1)
from contador_lineas.core.arbol.nodo import Nodo # BORRADA
from contador_lineas.config.node_types import (
    PARENT_NODE_TYPES,
    COMMENT_NODE_TYPES,
    NO_NESTED_ALLOWED
) # BORRADA (las 5 líneas previas cuentan como 1)
from contador_lineas.models.nodos import TipoNodo # BORRADA


class VerificadorEstandarCodigo:
    """
    Verifica el cumplimiento de estándares de código en el árbol sintáctico.

    Methods:
        es_arbol_sintactico_valido(self, raiz: Nodo) -> tuple[bool, str]: 
            Valida si el árbol cumple los estándares

    Example:
        >>> verificador = VerificadorEstandarCodigo()
        >>> es_valido, mensaje = verificador.es_arbol_sintactico_valido(raiz)
    """
    
    def __init__(self):
        pass

    def es_arbol_sintactico_valido(self, raiz: Nodo) -> tuple[bool, str]:
        """
        Verifica si el árbol sintáctico cumple con los estándares de código.

        Args:
            raiz (Nodo): Nodo raíz del árbol a validar

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)

        Example:
            >>> es_valido, mensaje = verificador.es_arbol_sintactico_valido(
                raiz
            )
        """
        return self._validar_nodo(raiz)
    
    def _validar_nodo(self, nodo: Nodo) -> tuple[bool, str]:
        """
        Valida recursivamente un nodo y sus hijos con los estándares de código.

        Args:
            nodo (Nodo): Nodo a validar con sus hijos

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)

        Example:
            >>> es_valido, mensaje = verificador._validar_nodo(nodo_raiz)
            >>> print(es_valido, mensaje)
            False "No se permiten expresiones lambda"
        """
        try:
            if nodo.tipo == TipoNodo.ROOT and len(nodo.hijos) == 0:
                return False, "El archivo debe tener al menos una línea de \
                código"

            if nodo.tipo in PARENT_NODE_TYPES and len(nodo.hijos) == 0:
                return False, f"La estructura {nodo.tipo} debe tener contenido"

            if (nodo.tipo not in COMMENT_NODE_TYPES and 
                    self._tiene_multiples_declaraciones(nodo.contenido)):
                return False, "No se permiten varias declaraciones en una \
                línea"

            if (nodo.tipo not in COMMENT_NODE_TYPES and 
                    self._tiene_operadores_anidados(nodo)):
                return False, "No se permiten operadores \
                ternarios/comprehension/generator anidados"

            if (nodo.tipo not in COMMENT_NODE_TYPES and 
                    self._tiene_expresion_lambda(nodo.contenido)):
                return False, "No se permiten expresiones lambda"

            for hijo in nodo.hijos:
                es_valido, error = self._validar_nodo(hijo)
                if not es_valido:
                    return False, error

            return True, ""
        except Exception as e:
            return False, f"Error al validar nodo: {str(e)}"
    
    @staticmethod
    def _tiene_multiples_declaraciones(contenido: str) -> bool:
        """
        Verifica si una línea contiene múltiples instrucciones con punto y \
        coma.

        Args:
            contenido (str): Línea de código a analizar

        Returns:
            bool: True si contiene múltiples declaraciones, False en caso \
            contrario

        Example:
            >>> tiene = verificador._tiene_multiples_declaraciones("x = 1; y = \
            2")
            >>> print(tiene)
            True
        """
        en_comilla_simple = False
        en_comilla_doble = False

        for i, caracter in enumerate(contenido):
            if caracter == "'" and not en_comilla_doble:
                en_comilla_simple = not en_comilla_simple
            elif caracter == '"' and not en_comilla_simple:
                en_comilla_doble = not en_comilla_doble

            if caracter == ';' and not en_comilla_simple and not \
            en_comilla_doble:
                contenido_posterior = contenido[i+1:].strip()
                if (contenido_posterior and \
                (contenido_posterior.startswith('"""')
                        or contenido_posterior.startswith("'''"))):
                    return True
                if (contenido_posterior and 
                        not contenido_posterior.startswith('#')):
                    return True

        return False

    @staticmethod
    def _tiene_operadores_anidados(nodo: Nodo) -> bool:
        """
        Verifica si la línea contiene operadores ternarios o comprensiones \
        anidadas.

        Args:
            nodo (Nodo): Nodo que contiene el código a analizar

        Returns:
            bool: True si contiene operadores anidados, False en caso contrario

        Example:
            >>> tiene = verificador._tiene_operadores_anidados(nodo)
            >>> print(tiene)
            True
        """
        if nodo.tipo in NO_NESTED_ALLOWED:
            resultado = AnalizadorExpresiones().analizar(nodo.contenido, 
                                                         nodo.tipo)
            if len(resultado.expresiones_anidadas) > 0:
                return True
        return False

    @staticmethod
    def _tiene_expresion_lambda(contenido: str) -> bool:
        """
        Verifica si la línea contiene una expresión lambda.

        Args:
            contenido (str): Línea de código a analizar

        Returns:
            bool: True si contiene una expresión lambda, False en caso \
            contrario

        Example:
            >>> tiene = verificador._tiene_expresion_lambda("lambda x: x + 1")
            >>> print(tiene)
            True
        """
        posicion = 0
        while True:
            posicion = AnalizadorCadenas.encontrar_sin_comillas(
                contenido, 'lambda ', posicion)
            if posicion == -1:
                return False

            resto = contenido[posicion + 6:].strip()
            if not resto:
                return False

            posicion_dos_puntos = AnalizadorCadenas.encontrar_sin_comillas(
                contenido, ':', posicion)
            if posicion_dos_puntos == -1:
                posicion += 6
                continue

            despues_dos_puntos = contenido[posicion_dos_puntos + 1:].strip()
            if not despues_dos_puntos or despues_dos_puntos.startswith('#'):
                posicion += 6
                continue

            return True
