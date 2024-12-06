"""
Nombre del módulo: analizador_expresiones.py
Ruta: src/core/analyzers/analizador_expresiones.py
Descripción: Analiza expresiones ternarias y comprehensions en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - models.nodos.InformacionExpresion
    - models.nodos.TipoNodo
    - core.analizadores.analizador_comprehension.AnalizadorComprehension
    - core.analizadores.analizador_ternario.AnalizadorTernario

Uso:
    from core.analizadores.analizador_expresiones import AnalizadorExpresiones
    
    analizador = AnalizadorExpresiones()
    info = analizador.analizar(codigo, TipoNodo.TERNARY)

Notas:
    - Procesa expresiones ternarias y comprehensions
    - Retorna None si la expresión no es válida
"""

from analizador_cambios.core.analizadores.analizador_comprehension import (
    AnalizadorComprehension
) # AÑADIDA EN UN 0.91% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.analizadores.analizador_ternario import (
    AnalizadorTernario
) # AÑADIDA EN UN 0.91% (las 3 líneas previas cuentan como 1)
from analizador_cambios.models.nodos import InformacionExpresion, TipoNodo # AÑADIDA EN UN 0.88%


class AnalizadorExpresiones:
    """
    Analizador de expresiones ternarias y comprehensions en código Python.

    Detecta y extrae información sobre expresiones condicionales ternarias
    y diferentes tipos de comprehensions.

    Attributes:
        analizador_ternario (AnalizadorTernario): Analiza expresiones ternarias
        analizador_comprehension (AnalizadorComprehension): Analiza \
        comprehensions

    Methods:
        analizar(codigo: str, tipo_nodo: TipoNodo) -> InformacionExpresion:
            Analiza una expresión y extrae su información.

    Example:
        >>> analizador = AnalizadorExpresiones()
        >>> info = analizador.analizar("x if y else z", TipoNodo.TERNARY)
        >>> info
        TipoNodo.TERNARY
    """
    def __init__(self) -> None:
        self.analizador_ternario = AnalizadorTernario()
        self.analizador_comprehension = AnalizadorComprehension()

    def analizar(
            self,
            codigo: str,
            tipo_nodo: TipoNodo) -> InformacionExpresion:
        """
        Analiza un ternario, comprehension o generator y determina si existe \
        anidamiento

        Args:
            codigo (str): Código fuente a analizar
            tipo_nodo (TipoNodo): Tipo de expresión a buscar

        Returns:
            InformacionExpresion: Información de la expresión analizada y sus \
            anidados

        Example:
            >>> analizar("[x for x in range(5)]", TipoNodo.LIST_COMPREHENSION)
            InformacionExpresion(tipo=TipoNodo.LIST_COMPREHENSION, ...)
        """
        if tipo_nodo == TipoNodo.TERNARY:
            resultado = self.analizador_ternario.analizar_ternario(codigo)
        else:
            resultado = \
            self.analizador_comprehension.procesar_comprehension(codigo)
        
        if not resultado:
            return InformacionExpresion(
                tipo=tipo_nodo,
                expresiones_anidadas=[],
                posicion_inicial=0,
                posicion_final=len(codigo),
                expresion=codigo
            )
        return resultado
