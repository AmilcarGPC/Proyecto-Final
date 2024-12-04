"""
Nombre del módulo: analizador_ternario.py
Ruta: src/core/analyzers/analizador_ternario.py
Descripción: Analiza y procesa expresiones ternarias en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - core.analizadores.analizador_cadenas.AnalizadorCadenas
    - core.analizadores.analizador_corchetes.AnalizadorCorchetes
    - core.analizadores.buscar_y_extraer_anidados.BuscarYExtraerAnidados
    - models.nodos.InformacionExpresion
    - utils.node_analyzer.TipoNodoAnalyzer

Uso:
    from core.analizadores.analizador_ternario import AnalizadorTernario
    
    analizador = AnalizadorTernario()
    info = analizador.analizar_ternario("x if y else z")

Notas:
    - Procesa expresiones ternarias simples y anidadas
    - Retorna None si no encuentra expresión ternaria válida
"""

from typing import List, Optional

from contador_lineas.core.analizadores.analizador_cadenas import AnalizadorCadenas
from contador_lineas.core.analizadores.analizador_corchetes import AnalizadorCorchetes
from contador_lineas.core.analizadores.buscar_y_extraer_anidados import BuscarYExtraerAnidados
from contador_lineas.models.nodos import InformacionExpresion, TipoNodo
from contador_lineas.utils.node_analyzer import TipoNodoAnalyzer


class AnalizadorTernario:
    """
    Analizador de expresiones ternarias en código Python.

    Procesa y extrae información sobre operadores ternarios,
    incluyendo expresiones anidadas.

    Attributes:
        analizador_cadenas (AnalizadorCadenas): Analiza cadenas de texto
        analizador_corchetes (AnalizadorCorchetes): Procesa pares de corchetes
        analizador_tipo (TipoNodoAnalyzer): Analiza tipos de nodos
        buscar_y_extraer_anidados (BuscarYExtraerAnidados): Extrae expresiones

    Methods:
        analizar_ternario(codigo: str, posicion_inicial: int) -> Optional[InformacionExpresion]:
            Determina si una expresión ternaria contiene anidaciones

    Example:
        >>> analizador = AnalizadorTernario()
        >>> info = analizador.analizar_ternario("x if y else z")
        >>> info.tipo
        TipoNodo.TERNARY
    """
    
    def __init__(self):
        self.analizador_cadenas = AnalizadorCadenas()
        self.analizador_corchetes = AnalizadorCorchetes()
        self.analizador_tipo = TipoNodoAnalyzer()
        self.buscar_y_extraer_anidados = BuscarYExtraerAnidados()

    def analizar_ternario(
            self,
            codigo: str,
            posicion_inicial: int = 0
        ) -> Optional[InformacionExpresion]:
        """
        Analiza una expresión ternaria y extrae su información, así como sus anidados.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición donde empezar búsqueda

        Returns:
            Optional[InformacionExpresion]: Información de la expresión o None

        Example:
            >>> analizar_ternario("x if y else z", 0)
        """
        if not self._es_operacion_valida(codigo):
            return None

        posiciones = self._encontrar_posiciones_operadores(codigo, posicion_inicial)
        if not posiciones:
            return None

        posicion_final = self._calcular_posicion_final(codigo, posiciones)
        expresiones_anidadas = self._procesar_expresiones_anidadas(
            codigo, posiciones, posicion_final
        )

        return self._crear_expression_info(
            codigo, posicion_inicial, posicion_final, expresiones_anidadas
        )
    
    def _es_operacion_valida(self, codigo: str) -> bool:
        """
        Verifica si el código contiene una expresión ternaria válida.

        Args:
            codigo (str): Código fuente a analizar

        Returns:
            bool: True si es una operación ternaria válida
        """
        try:
            return self.analizador_tipo.check_special_operations(codigo)
        except Exception:
            return False
        
    def _encontrar_posiciones_operadores(
            self, codigo: str, posicion_inicial: int
        ) -> Optional[dict]:
        """
        Obtiene las posiciones de los operadores if/else en el código.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición donde iniciar búsqueda

        Returns:
            Optional[dict]: Diccionario con posiciones o None si no encuentra
        """
        posicion_if = self.analizador_cadenas.encontrar_sin_comillas(
            codigo, ' if ', posicion_inicial
        )
        if posicion_if == -1:
            return None

        posicion_else = self.analizador_cadenas.encontrar_sin_comillas(
            codigo, ' else ', posicion_if
        )
        if posicion_else == -1:
            return None

        return {
            'if': posicion_if,
            'else': posicion_else,
            'siguiente_if': codigo.find(' if ', posicion_else),
            'siguiente_else': codigo.find(' else ', posicion_else + 6)
        }

    def _calcular_posicion_final(
            self, codigo: str, posiciones: dict
        ) -> int:
        """
        Calcula la posición donde termina la expresión ternaria.

        Args:
            codigo (str): Código fuente a analizar
            posiciones (dict): Posiciones de operadores encontrados

        Returns:
            int: Posición final de la expresión
        """
        if self._tiene_ternario_anidado(posiciones):
            return self._procesar_ternario_anidado(codigo, posiciones)
        return self.analizador_corchetes.encontrar_limite_expresion(
            codigo, posiciones['else'] + 6
        )

    def _tiene_ternario_anidado(self, posiciones: dict) -> bool:
        """
        Verifica si existe un ternario anidado después del else.

        Args:
            posiciones (dict): Posiciones de operadores encontrados

        Returns:
            bool: True si existe ternario anidado
        """
        return (posiciones['siguiente_if'] != -1 and 
                posiciones['siguiente_else'] != -1)

    def _procesar_ternario_anidado(
            self, codigo: str, posiciones: dict
        ) -> int:
        """
        Procesa un ternario anidado y calcula su posición final.

        Args:
            codigo (str): Código fuente a analizar
            posiciones (dict): Posiciones de operadores encontrados

        Returns:
            int: Posición final del ternario anidado
        """
        ternario_anidado = self.analizar_ternario(
            codigo[posiciones['else'] + 6:], 0
        )
        return posiciones['else'] + 6 + (
            ternario_anidado.posicion_final if ternario_anidado else 0
        )

    def _procesar_expresiones_anidadas(
            self, codigo: str, posiciones: dict, posicion_final: int
        ) -> List[InformacionExpresion]:
        """
        Extrae todas las expresiones anidadas del ternario.

        Args:
            codigo (str): Código fuente a analizar
            posiciones (dict): Posiciones de operadores encontrados
            posicion_final (int): Posición final de la expresión

        Returns:
            List[InformacionExpresion]: Lista de expresiones anidadas encontradas
        """
        expresiones = []
        self._agregar_expresiones_condicion(
            codigo, posiciones, expresiones
        )
        self._agregar_expresiones_valor(
            codigo, posiciones, expresiones
        )
        self._agregar_expresiones_else(
            codigo, posiciones, posicion_final, expresiones
        )
        return expresiones

    def _crear_expression_info(
            self, codigo: str, inicio: int, fin: int, 
            expresiones_anidadas: List[InformacionExpresion]
        ) -> InformacionExpresion:
        """
        Crea un objeto InformacionExpresion con la información del ternario.

        Args:
            codigo (str): Código fuente analizado
            inicio (int): Posición inicial
            fin (int): Posición final
            expresiones_anidadas (List[InformacionExpresion]): Expresiones encontradas

        Returns:
            InformacionExpresion: Objeto con información del ternario
        """
        return InformacionExpresion(
            tipo=TipoNodo.TERNARY,
            expresiones_anidadas=expresiones_anidadas,
            posicion_inicial=inicio,
            posicion_final=fin,
            expresion=codigo[inicio:fin]
        )
    
    def _agregar_expresiones_condicion(
            self,
            codigo: str,
            posiciones: dict,
            expresiones: List[InformacionExpresion]
        ) -> None:
        """
        Agrega expresiones anidadas encontradas en la condición del ternario.

        Args:
            codigo (str): Código fuente a analizar
            posiciones (dict): Diccionario con posiciones de operadores
            expresiones (List[InformacionExpresion]): Lista donde agregar expresiones
        """
        try:
            segmento = codigo[posiciones['if'] + 4:posiciones['else']]
            expresiones.extend(self._encontrar_expresiones(segmento))
        except Exception:
            return

    def _agregar_expresiones_valor(
            self,
            codigo: str,
            posiciones: dict,
            expresiones: List[InformacionExpresion]
        ) -> None:
        """
        Agrega expresiones anidadas encontradas en el valor antes del if.

        Args:
            codigo (str): Código fuente a analizar
            posiciones (dict): Diccionario con posiciones de operadores
            expresiones (List[InformacionExpresion]): Lista donde agregar expresiones
        """
        try:
            segmento = codigo[:posiciones['if']]
            expresiones.extend(self._encontrar_expresiones(segmento))
        except Exception:
            return

    def _agregar_expresiones_else(
            self,
            codigo: str,
            posiciones: dict,
            posicion_final: int,
            expresiones: List[InformacionExpresion]
        ) -> None:
        """
        Agrega expresiones anidadas encontradas en la parte else del ternario.

        Args:
            codigo (str): Código fuente a analizar
            posiciones (dict): Diccionario con posiciones de operadores
            posicion_final (int): Posición final de la expresión
            expresiones (List[InformacionExpresion]): Lista donde agregar expresiones
        """
        try:
            expresion_else = codigo[posiciones['else'] + 6:posicion_final]
            if ' if ' in expresion_else:
                if ternario := self.analizar_ternario(expresion_else):
                    expresiones.append(ternario)
            else:
                expresiones.extend(self._encontrar_expresiones(expresion_else))
        except Exception:
            return
        
    def _encontrar_expresiones(self, codigo: str) -> List[InformacionExpresion]:
        """
        Busca expresiones anidadas en el código.

        Args:
            codigo (str): Código fuente a analizar

        Returns:
            List[InformacionExpresion]: Lista de expresiones encontradas

        Example:
            >>> _encontrar_expresiones("x if y else z")
        """
        expresiones = []
        if ternario := self.analizar_ternario(codigo):
            expresiones.append(ternario)
        expresiones.extend(
            self.buscar_y_extraer_anidados.buscar_comprehensions_anidadas( codigo )
        )
        return expresiones