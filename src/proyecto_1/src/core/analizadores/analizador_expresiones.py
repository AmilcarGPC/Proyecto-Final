"""
Nombre del módulo: analizador_expresiones.py
Ruta: src/core/analyzers/analizador_expresiones.py
Descripción: Analiza expresiones ternarias y comprehensions en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18/11/2024
Última Actualización: 18/11/2024

Dependencias:
    - models.nodes.ExpressionInfo
    - models.nodes.NodeType
    - core.analizadores.analizador_comprehension.AnalizadorComprehension
    - core.analizadores.analizador_ternario.AnalizadorTernario

Uso:
    from core.analizadores.analizador_expresiones import AnalizadorExpresiones
    
    analizador = AnalizadorExpresiones()
    info = analizador.analizar(codigo, NodeType.TERNARY)

Notas:
    - Procesa expresiones ternarias y comprehensions
    - Retorna None si la expresión no es válida
"""
from core.analizadores.analizador_comprehension import AnalizadorComprehension
from core.analizadores.analizador_ternario import AnalizadorTernario
from models.nodes import ExpressionInfo, NodeType


class AnalizadorExpresiones:
    """
    Analizador de expresiones ternarias y comprehensions en código Python.

    Detecta y extrae información sobre expresiones condicionales ternarias
    y diferentes tipos de comprehensions.

    Attributes:
        analizador_ternario (AnalizadorTernario): Analiza expresiones ternarias
        analizador_comprehension (AnalizadorComprehension): Analiza comprehensions

    Methods:
        analizar(codigo: str, tipo_nodo: NodeType) -> ExpressionInfo:
            Analiza una expresión y extrae su información.

    Example:
        >>> analizador = AnalizadorExpresiones()
        >>> info = analizador.analizar("x if y else z", NodeType.TERNARY)
        >>> info
        NodeType.TERNARY
    """
    def __init__(self) -> None:
        self.analizador_ternario = AnalizadorTernario()
        self.analizador_comprehension = AnalizadorComprehension()

    def analizar(self, codigo: str, tipo_nodo: NodeType) -> ExpressionInfo:
        """
        Analiza un ternario, comprehension o generator y determina si existe anidamiento

        Args:
            codigo (str): Código fuente a analizar
            tipo_nodo (NodeType): Tipo de expresión a buscar

        Returns:
            ExpressionInfo: Información de la expresión analizada y sus anidados

        Example:
            >>> analizar("[x for x in range(5)]", NodeType.LIST_COMPREHENSION)
            ExpressionInfo(type=NodeType.LIST_COMPREHENSION, ...)
        """
        if tipo_nodo == NodeType.TERNARY:
            resultado = self.analizador_ternario.analizar_ternario(codigo)
        else:
            resultado = self.analizador_comprehension.procesar_comprehension(codigo)
        
        if not resultado:
            return ExpressionInfo(
                type=tipo_nodo,
                nested_expressions=[],
                start_pos=0,
                end_pos=len(codigo),
                expression=codigo
            )
        return resultado