"""
Nombre del módulo: buscar_y_extraer_anidados.py
Ruta: contador_lineas/core/analizadores/buscar_y_extraer_anidados.py
Descripción: Analiza y extrae expresiones anidadas en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - core.analizadores.analizador_cadenas.AnalizadorCadenas
    - core.analizadores.analizador_corchetes.AnalizadorCorchetes
    - core.analizadores.analizador_ternario.AnalizadorTernario
    - core.constantes.CORCHETES
    - models.nodos.InformacionExpresion

Uso:
    from contador_lineas.core.analizadores.buscar_y_extraer_anidados import (
        BuscarYExtraerAnidados
    )
    
    analizador = BuscarYExtraerAnidados()
    expresiones = analizador.extraer_expresiones_anidadas(codigo, pos_for, 
                                                          pos_final)

Notas:
    - Procesa expresiones ternarias y comprehensions anidadas
    - Retorna lista vacía si no encuentra expresiones
"""

from typing import List

from contador_lineas.core.analizadores.analizador_cadenas import (
    AnalizadorCadenas
)
from contador_lineas.core.analizadores.analizador_corchetes import (
    AnalizadorCorchetes
)
from contador_lineas.core.constantes import CORCHETES
from contador_lineas.models.nodos import InformacionExpresion


class BuscarYExtraerAnidados:
    """
    Busca y extrae expresiones anidadas en código Python.

    Analiza el código fuente para encontrar expresiones ternarias y 
    comprehensions anidadas dentro de otras expresiones.

    Attributes:
        analizador_cadenas (AnalizadorCadenas): Analiza cadenas de texto
        analizador_corchetes (AnalizadorCorchetes): Procesa pares de corchetes

    Methods:
        extraer_expresiones_anidadas(
                codigo: str, 
                posicion_for: int, 
                posicion_final: int) -> List[InformacionExpresion]:
            Extrae expresiones anidadas del código dado.
        buscar_comprehensions_anidadas(
                codigo: str) -> List[InformacionExpresion]:
            Busca comprehensions anidadas en una cadena de texto.
            
    Example:
        >>> analizador = BuscarYExtraerAnidados()
        >>> analizador.extraer_expresiones_anidadas(
                "[x for x in range(5)]", 1, 10
            )
    """

    def __init__(self):
        self.analizador_cadenas = AnalizadorCadenas()
        self.analizador_corchetes = AnalizadorCorchetes()

    def extraer_expresiones_anidadas(
            self, codigo: str, posicion_for: int, posicion_final: int
        ) -> List[InformacionExpresion]:
        """
        Extrae expresiones anidadas del código dado.

        Args:
            codigo (str): Código fuente a analizar
            posicion_for (int): Posición del 'for' en el código
            posicion_final (int): Posición final del análisis

        Returns:
            List[InformacionExpresion]: Lista de expresiones anidadas 
                                        encontradas

        Example:
            >>> extraer_expresiones_anidadas("[x for x in range(5)]", 1, 10)
        """
        expresiones_anidadas = []

        # Analizamos la parte antes del 'for' primero ya que puede contener
        # expresiones complejas como resultados de otras comprehensions
        expresion_previa = codigo[:posicion_for].strip()
        if expresion_previa:
            expresiones_anidadas.extend(
                self.buscar_comprehensions_anidadas(expresion_previa)
            )
            expresiones_anidadas.extend(
                self._buscar_ternarios_anidados(expresion_previa)
            )

        # La parte después del 'in' puede contener iterables complejos como
        # otras comprehensions o generadores
        if posicion_in := self.analizador_cadenas.encontrar_sin_comillas(
            codigo, ' in ', posicion_for
        ):
            expresion_iteracion = codigo[posicion_in + 4:posicion_final]
            expresiones_anidadas.extend(
                self.buscar_comprehensions_anidadas(expresion_iteracion)
            )
            expresiones_anidadas.extend(
                self._buscar_ternarios_anidados(expresion_iteracion)
            )

        expresion_for = codigo[posicion_for:posicion_final]
        if posicion_if := self.analizador_cadenas.encontrar_sin_comillas(
            expresion_for, ' if '
        ):
            if posicion_if != -1:
                expresion_condicion = expresion_for[posicion_if + 4:]
                expresiones_anidadas.extend(
                    self.buscar_comprehensions_anidadas(expresion_condicion)
                )
                expresiones_anidadas.extend(
                    self._buscar_ternarios_anidados(expresion_condicion)
                )
        return expresiones_anidadas

    def buscar_comprehensions_anidadas(
            self,
            codigo: str) -> List[InformacionExpresion]:
        """
        Busca comprehensions anidadas en el código.

        Args:
            codigo (str): Código fuente a analizar

        Returns:
            List[InformacionExpresion]: Lista de comprehensions encontradas

        Example:
            >>> buscar_comprehensions_anidadas(
                    "[x for x in [y for y in range(5)]]"
                )
        """
        expresiones_anidadas = []
        posicion_actual = 0

        while posicion_actual < len(codigo):
            # Solo procesamos corchetes que no estén dentro de cadenas de texto
            # para evitar falsos positivos
            if (codigo[posicion_actual] in CORCHETES and
                not self.analizador_cadenas.esta_en_cadena(
                    codigo, posicion_actual
                )):
                # Buscamos el corchete de cierre respectivo para asegurarnos de
                # procesar la expresión completa incluyendo anidamientos
                posicion_final = \
                    self.analizador_corchetes.encontrar_par_corchetes(
                    codigo,
                    posicion_actual,
                    (codigo[posicion_actual],
                     CORCHETES[codigo[posicion_actual]])
                )

                if posicion_final != -1:
                    segmento = codigo[posicion_actual:posicion_final + 1]
                    # La presencia de 'for' distingue una comprehension de una
                    # simple lista/conjunto/generador
                    posicion_for = \
                        self.analizador_cadenas.encontrar_sin_comillas(
                        segmento, ' for '
                    )

                    if posicion_for != -1:
                        # Procesamos recursivamente para encontrar más
                        # anidamientos
                        expresion_comprehension = InformacionExpresion(
                            tipo=self._obtener_tipo_comprehension(
                                codigo[posicion_actual]
                            ),
                            posicion_inicial=posicion_actual,
                            posicion_final=posicion_final + 1,
                            expresion=segmento,
                            expresiones_anidadas =
                            self.extraer_expresiones_anidadas(
                                segmento,
                                posicion_for,
                                len(segmento)
                            )
                        )
                        expresiones_anidadas.append(expresion_comprehension)
                        # Saltamos al final de esta comprehension para evitar
                        # procesar sus elementos internos como expresiones
                        # separadas
                        posicion_actual = posicion_final + 1
                        continue
            posicion_actual += 1
        return expresiones_anidadas

    def _buscar_ternarios_anidados(
            self,
            codigo: str) -> List[InformacionExpresion]:
        """
        Busca operadores ternarios anidados en el código.

        Args:
            codigo (str): Código fuente a analizar

        Returns:
            List[InformacionExpresion]: Lista de expresiones ternarias 
                                        encontradas

        Example:
            >>> _buscar_ternarios_anidados("x if y else z")
        """
        # Importamos aquí para evitar ciclos de importación
        from contador_lineas.core.analizadores.analizador_ternario import (
            AnalizadorTernario
        )

        expresion_ternaria = AnalizadorTernario().analizar_ternario(codigo)
        if not expresion_ternaria:
            return []
        return [expresion_ternaria]

    def _obtener_tipo_comprehension(self, corchete: str) -> str:
        """
        Obtiene el tipo de comprehension según el corchete.

        Args:
            corchete (str): Caracter de corchete inicial

        Returns:
            str: Tipo de comprehension identificado

        Example:
            >>> _obtener_tipo_comprehension('[')
            'comprehension_lista'
        """
        return {
            '[': 'comprehension_lista',
            '{': 'comprehension_conjunto',
            '(': 'expresion_generadora'
        }.get(corchete, 'desconocido')
