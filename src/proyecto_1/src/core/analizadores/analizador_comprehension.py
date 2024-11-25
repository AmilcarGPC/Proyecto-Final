"""
Nombre del módulo: analizador_comprehension.py
Ruta: src/core/analyzers/analizador_comprehension.py
Descripción: Analiza y procesa expresiones de comprehensions en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18/11/2024
Última Actualización: 18/11/2024

Dependencias:
    - core.analizadores.analizador_corchetes.AnalizadorCorchetes
    - core.analizadores.analizador_cadenas.AnalizadorCadenas
    - core.analizadores.buscar_y_extraer_anidados.BuscarYExtraerAnidados
    - core.constantes.CORCHETES, TIPOS_COMPREHENSION
    - models.nodes.ExpressionInfo, NodeType
    - utils.node_analyzer.NodeTypeAnalyzer

Uso:
    from core.analizadores.analizador_comprehension import AnalizadorComprehension
    
    analizador = AnalizadorComprehension()
    info = analizador.procesar_comprehension(codigo, posicion_inicial)

Notas:
    - Analiza list, dict, set comprehensions y generator expressions
    - Detecta y maneja expresiones anidadas
"""
from core.analizadores.analizador_corchetes import AnalizadorCorchetes
from core.analizadores.buscar_y_extraer_anidados import BuscarYExtraerAnidados
from core.analizadores.analizador_cadenas import AnalizadorCadenas
from core.constantes import TIPOS_COMPREHENSION, CORCHETES
from models.nodes import ExpressionInfo, NodeType
from utils.node_analyzer import NodeTypeAnalyzer


class AnalizadorComprehension:
    """
    Analiza y procesa expresiones de comprensión en código Python.

    Detecta y extrae información sobre list, dict, set comprehensions
    y generator expressions.

    Attributes:
        analizador_cadenas (AnalizadorCadenas): Analiza cadenas de texto
        analizador_corchetes (AnalizadorCorchetes): Procesa pares de corchetes
        analizador_tipo (NodeTypeAnalyzer): Determina tipos de nodos
        buscar_y_extraer (BuscarYExtraerAnidados): Extrae expresiones anidadas

    Methods:
        procesar_comprehension(codigo: str, posicion_inicial: int) -> ExpressionInfo | None:
            Determina si una expresión comprehension o generator contiene anidaciones

    Example:
        >>> analizador = AnalizadorComprehension()
        >>> info = analizador.procesar_comprehension("[x for x in range(5)]", 0)
        >>> info
        NodeType.LIST_COMPREHENSION
    """
    def __init__(self):
        self.analizador_cadenas = AnalizadorCadenas()
        self.analizador_corchetes = AnalizadorCorchetes()
        self.analizador_tipo = NodeTypeAnalyzer()
        self.buscar_y_extraer = BuscarYExtraerAnidados()

    def procesar_comprehension(self, codigo: str, posicion_inicial: int = 0) -> ExpressionInfo | None:
        """
        Procesa una expresión de comprensión y extrae su información, así como sus anidados.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición donde inicia la búsqueda

        Returns:
            ExpressionInfo | None: Información de la expresión o None si no es válida

        Example:
            >>> self.procesar_comprehension("[x for x in range(5)]", 0)
            ExpressionInfo(type=NodeType.LIST_COMPREHENSION, ...)
        """
        try:
            if not (self.analizador_tipo.check_comprehensions(codigo)):
                return None

            posiciones_for = []
            posicion = posicion_inicial
            while True:
                posicion = self.analizador_cadenas.encontrar_sin_comillas(codigo, ' for ', posicion)
                if posicion == -1:
                    break
                if not self.analizador_cadenas.esta_en_cadena(codigo, posicion):
                    posiciones_for.append(posicion)
                posicion += 5

            if not posiciones_for:
                return None

            posicion_for_externo = posiciones_for[0]
            profundidad_minima = float('inf')
            
            for posicion in posiciones_for:
                profundidad = 0
                for i in range(posicion_inicial, posicion):
                    if codigo[i] in '([{':
                        profundidad += 1
                    elif codigo[i] in ')]}':
                        profundidad -= 1
                if profundidad < profundidad_minima:
                    profundidad_minima = profundidad
                    posicion_for_externo = posicion

            posicion_final = self._encontrar_fin_comprehension(codigo, posicion_inicial)
            expresiones_anidadas = self.buscar_y_extraer.extraer_expresiones_anidadas(
                codigo, 
                posicion_for_externo, 
                posicion_final
            )

            return ExpressionInfo(
                type=self._encontrar_tipo_principal(codigo),
                nested_expressions=expresiones_anidadas,
                start_pos=posicion_inicial,
                end_pos=posicion_final,
                expression=codigo[posicion_inicial:posicion_final]
            )
        except IndexError:
            return None
        except ValueError:
            return None
        
    def _encontrar_tipo_principal(self, codigo: str) -> NodeType:
        """
        Determina el tipo de comprehension basado en sus caracteres.

        Args:
            codigo (str): Código fuente a analizar

        Returns:
            NodeType: Tipo de comprehension encontrado

        Example:
            >>> self._encontrar_tipo_principal("[x for x in range(5)]")
            NodeType.LIST_COMPREHENSION
        """
        for caracter in codigo:
            if caracter in TIPOS_COMPREHENSION:
                return TIPOS_COMPREHENSION[caracter]
    
    def _encontrar_fin_comprehension(self, codigo: str, posicion_inicial: int) -> int:
        """
        Encuentra la posición final de una expresión de comprensión.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición donde inicia la búsqueda

        Returns:
            int: Posición final de la expresión

        Example:
            >>> self._encontrar_fin_comprehension("[x for x in range(5)]", 0)
            21
        """
        for corchete_apertura, corchete_cierre in CORCHETES.items():
            if corchete_apertura in codigo[posicion_inicial:]:
                posicion_corchete = codigo.find(corchete_apertura, posicion_inicial)
                return self.analizador_corchetes.encontrar_par_corchetes(
                    codigo, 
                    posicion_corchete, 
                    (corchete_apertura, corchete_cierre)
                ) + 1
        return len(codigo)