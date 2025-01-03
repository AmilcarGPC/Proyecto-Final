"""
Nombre del módulo: analizador_comprehension.py
Ruta: contador_lineas/core/analizadores/analizador_comprehension.py
Descripción: Analiza y procesa expresiones de comprehensions en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - contador_lineas.core.analizadores.analizador_corchetes.AnalizadorCorchetes
    - contador_lineas.core.analizadores.analizador_cadenas.AnalizadorCadenas
    - contador_lineas.core.analizadores.buscar_y_extraer_anidados.BuscarYExtraerAnidados
    - contador_lineas.core.constantes.CORCHETES, TIPOS_COMPREHENSION
    - contador_lineas.models.nodos.InformacionExpresion, TipoNodo
    - contador_lineas.utils.analizador_nodos.AnalizadorTipoNodo

Uso:
    from contador_lineas.core.analizadores.analizador_comprehension import (
        AnalizadorComprehension
    )
    
    analizador = AnalizadorComprehension()
    info = analizador.procesar_comprehension(codigo, posicion_inicial)

Notas:
    - Analiza list, dict, set comprehensions y generator expressions
    - Detecta y maneja expresiones anidadas
"""

from contador_lineas.core.analizadores.analizador_corchetes import (
    AnalizadorCorchetes
)
from contador_lineas.core.analizadores.buscar_y_extraer_anidados import (
    BuscarYExtraerAnidados
)
from contador_lineas.core.analizadores.analizador_cadenas import (
    AnalizadorCadenas
)
from contador_lineas.core.constantes import TIPOS_COMPREHENSION, CORCHETES
from contador_lineas.models.nodos import InformacionExpresion, TipoNodo
from contador_lineas.core.arbol.analizador_nodos import AnalizadorTipoNodo


class AnalizadorComprehension:
    """
    Analiza y procesa expresiones de comprensión en código Python.

    Detecta y extrae información sobre list, dict, set comprehensions
    y generator expressions.

    Attributes:
        analizador_cadenas (AnalizadorCadenas): Analiza cadenas de texto
        analizador_corchetes (AnalizadorCorchetes): Procesa pares de corchetes
        analizador_tipo (AnalizadorTipoNodo): Determina tipos de nodos
        buscar_y_extraer (BuscarYExtraerAnidados): Extrae expresiones anidadas

    Methods:
        procesar_comprehension(
            codigo: str, 
            posicion_inicial: int) -> InformacionExpresion | None:
            Determina si una expresión comprehension o generator contiene 
            anidaciones

    Example:
        >>> analizador = AnalizadorComprehension()
        >>> info = analizador.procesar_comprehension("[x for x in range(5)]", 0)
        >>> info
        TipoNodo.LIST_COMPREHENSION
    """

    def __init__(self):
        self.analizador_cadenas = AnalizadorCadenas()
        self.analizador_corchetes = AnalizadorCorchetes()
        self.analizador_tipo = AnalizadorTipoNodo()
        self.buscar_y_extraer = BuscarYExtraerAnidados()

    def procesar_comprehension(
            self,
            codigo: str,
            posicion_inicial: int = 0) -> InformacionExpresion | None:
        """
        Procesa una expresión de comprensión y extrae su información, así como 
        sus anidados.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición donde inicia la búsqueda

        Returns:
            InformacionExpresion | None: Información de la expresión o None si 
                                         no es válida

        Example:
            >>> self.procesar_comprehension("[x for x in range(5)]", 0)
            InformacionExpresion(tipo=TipoNodo.LIST_COMPREHENSION, ...)
        """
        try:
            if not self.analizador_tipo.verificar_comprensiones(codigo):
                return None

            posiciones_for = []
            posicion = posicion_inicial

            # Buscamos todas las ocurrencias de 'for' fuera de cadenas "", '
            # Necesario para manejar comprehensions anidadas como:
            # [x for x in [y for y in range(5)]]
            while True:
                posicion = self.analizador_cadenas.encontrar_sin_comillas(
                    codigo, ' for ', posicion)
                if posicion == -1:
                    break
                if not self.analizador_cadenas.esta_en_cadena(codigo, posicion):
                    posiciones_for.append(posicion)
                posicion += 5

            if not posiciones_for:
                return None

            # Determinamos el 'for' más externo basado en la profundidad
            # Necesario para comprehensions anidadas y evitar falsos positivos
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

            posicion_final = self._encontrar_fin_comprehension(codigo,
                                                               posicion_inicial)
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
        # Iteramos sobre tipos de corchetes válidos ([], (), {})
        # Esto para manejar diferentes tipos de comprehensions y generators
        for corchete_apertura, corchete_cierre in CORCHETES.items():
            if corchete_apertura in codigo[posicion_inicial:]:
                posicion_corchete = codigo.find(corchete_apertura,
                                                posicion_inicial)
                # Usamos analizador_corchetes para manejar anidamiento correcto
                # Ej: [x for x in [(y,z) for y,z in pairs]]
                return self.analizador_corchetes.encontrar_par_corchetes(
                    codigo,
                    posicion_corchete,
                    (corchete_apertura, corchete_cierre)
                ) + 1
        return len(codigo)
