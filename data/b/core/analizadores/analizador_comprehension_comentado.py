"""
Nombre del módulo: analizador_comprehension.py
Ruta: src/core/analyzers/analizador_comprehension.py
Descripción: Analiza y procesa expresiones de comprehensions en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - core.analizadores.analizador_corchetes.AnalizadorCorchetes
    - core.analizadores.analizador_cadenas.AnalizadorCadenas
    - core.analizadores.buscar_y_extraer_anidados.BuscarYExtraerAnidados
    - core.constantes.CORCHETES, TIPOS_COMPREHENSION
    - models.nodos.InformacionExpresion, TipoNodo
    - utils.node_analyzer.TipoNodoAnalyzer

Uso:
    from core.analizadores.analizador_comprehension import (
        AnalizadorComprehension
    )
    
    analizador = AnalizadorComprehension()
    info = analizador.procesar_comprehension(codigo, posicion_inicial)

Notas:
    - Analiza list, dict, set comprehensions y generator expressions
    - Detecta y maneja expresiones anidadas
"""

from analizador_cambios.core.analizadores.analizador_corchetes import (
    AnalizadorCorchetes
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.91% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.analizadores.buscar_y_extraer_anidados import (
    BuscarYExtraerAnidados
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.91% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.analizadores.analizador_cadenas import (
    AnalizadorCadenas
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.9% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.constantes import TIPOS_COMPREHENSION, CORCHETES # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.89%
from analizador_cambios.models.nodos import InformacionExpresion, TipoNodo # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.88%
from analizador_cambios.utils.node_analyzer import TipoNodoAnalyzer # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.87%


class AnalizadorComprehension:
    """
    Analiza y procesa expresiones de comprensión en código Python.

    Detecta y extrae información sobre list, dict, set comprehensions
    y generator expressions.

    Attributes:
        analizador_cadenas (AnalizadorCadenas): Analiza cadenas de texto
        analizador_corchetes (AnalizadorCorchetes): Procesa pares de corchetes
        analizador_tipo (TipoNodoAnalyzer): Determina tipos de nodos
        buscar_y_extraer (BuscarYExtraerAnidados): Extrae expresiones anidadas

    Methods:
        procesar_comprehension(codigo: str, posicion_inicial: int) -> \
        InformacionExpresion | None:
            Determina si una expresión comprehension o generator contiene \
            anidaciones

    Example:
        >>> analizador = AnalizadorComprehension()
        >>> info = analizador.procesar_comprehension(
            "[x for x in range(5)]",
            0
        )
        >>> info
        TipoNodo.LIST_COMPREHENSION
    """
    
    def __init__(self):
        self.analizador_cadenas = AnalizadorCadenas()
        self.analizador_corchetes = AnalizadorCorchetes()
        self.analizador_tipo = TipoNodoAnalyzer()
        self.buscar_y_extraer = BuscarYExtraerAnidados()

    def procesar_comprehension(
            self,
            codigo: str,
            posicion_inicial: int = 0) -> InformacionExpresion | None:
        """
        Procesa una expresión de comprensión y extrae su información, así como \
        sus anidados.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición donde inicia la búsqueda

        Returns:
            InformacionExpresion | None: Información de la expresión o None si \
            no es válida

        Example:
            >>> self.procesar_comprehension("[x for x in range(5)]", 0)
            InformacionExpresion(tipo=TipoNodo.LIST_COMPREHENSION, .) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.98%
        """
        try:
            if not (self.analizador_tipo.check_comprehensions(codigo)):
                return None

            posiciones_for = []
            posicion = posicion_inicial
            while True:
                posicion = self.analizador_cadenas.encontrar_sin_comillas(
                    codigo,
                    ' for ',
                    posicion
                )
                if posicion == -1:
                    break
                if not self.analizador_cadenas.esta_en_cadena(codigo, \
                posicion):
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

            posicion_final = self._encontrar_fin_comprehension(
                codigo,
                posicion_inicial
            )
            expresiones_anidadas = \
            self.buscar_y_extraer.extraer_expresiones_anidadas(
                codigo, 
                posicion_for_externo, 
                posicion_final
            )

            return InformacionExpresion(
                tipo=self._encontrar_tipo_principal(codigo),
                expresiones_anidadas=expresiones_anidadas,
                posicion_inicial=posicion_inicial,
                posicion_final=posicion_final,
                expresion=codigo[posicion_inicial:posicion_final]
            )
        except IndexError:
            return None
        except ValueError:
            return None
        
    def _encontrar_tipo_principal(self, codigo: str) -> TipoNodo:
        """
        Determina el tipo de comprehension basado en sus caracteres.

        Args:
            codigo (str): Código fuente a analizar

        Returns:
            TipoNodo: Tipo de comprehension encontrado

        Example:
            >>> self._encontrar_tipo_principal("[x for x in range(5)]")
            TipoNodo.LIST_COMPREHENSION
        """
        for caracter in codigo:
            if caracter in TIPOS_COMPREHENSION:
                return TIPOS_COMPREHENSION[caracter]
    
    def _encontrar_fin_comprehension(
            self,
            codigo: str,
            posicion_inicial: int) -> int:
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
                posicion_corchete = codigo.find(
                    corchete_apertura,
                    posicion_inicial
                )
                return self.analizador_corchetes.encontrar_par_corchetes(
                    codigo, 
                    posicion_corchete, 
                    (corchete_apertura, corchete_cierre)
                ) + 1
        return len(codigo)
