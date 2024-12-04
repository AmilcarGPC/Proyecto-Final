"""
Nombre del módulo: analizador_corchetes.py
Ruta: contador_lineas/core/analizadores/analizador_corchetes.py
Descripción: Analiza y encuentra pares de corchetes y límites de expresiones en 
             código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 19-11-2024

Dependencias:
    - contador_lineas.core.constantes.CORCHETES

Uso:
    from contador_lineas.core.analizadores.analizador_corchetes import (
        AnalizadorCorchetes
    )
    
    analizador = AnalizadorCorchetes()
    posicion = analizador.encontrar_par_corchetes(
                   codigo, pos_inicial, ('(', ')'))

Notas:
    - Maneja paréntesis [] y ()
    - Retorna -1 si no encuentra el par correspondiente
"""

from typing import Tuple

from contador_lineas.core.constantes import CORCHETES


class AnalizadorCorchetes:
    """
    Analizador de corchetes y expresiones en código Python.

    Proporciona funcionalidad para encontrar pares de corchetes correspondientes
    y límites de expresiones en código fuente Python.

    Methods:
        encontrar_par_corchetes(
                codigo: str, 
                posicion_inicial: int, 
                corchetes: Tuple[str, str]) -> int:
            Encuentra la posición del corchete de cierre correspondiente.
        encontrar_limite_expresion(codigo: str, posicion_inicial: int) -> int:
            Encuentra el límite de una expresión en el código.

    Example:
        >>> analizador = AnalizadorCorchetes()
        >>> analizador.encontrar_par_corchetes("(x + y)", 0, ('(', ')'))
        6
    """

    @staticmethod
    def encontrar_par_corchetes(
            codigo: str,
            posicion_inicial: int,
            corchetes: Tuple[str, str]) -> int:
        """
        Encuentra la posición del corchete de cierre correspondiente.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición del corchete de apertura
            corchetes (Tuple[str, str]): Par de caracteres de apertura y cierre

        Returns:
            int: Posición del corchete de cierre o -1 si no se encuentra

        Example:
            >>> encontrar_par_corchetes("(x + y)", 0, ('(', ')'))
            6
        """
        try:
            caracter_apertura, caracter_cierre = corchetes
            # Usamos un contador para manejar corchetes anidados
            # El contador aumenta con cada apertura y disminuye con cada cierre
            contador = 1
            posicion = posicion_inicial + 1

            while posicion < len(codigo) and contador > 0:
                caracter_actual = codigo[posicion]
                # El manejo de anidamiento requiere actualizar el contador para
                # cada corchete encontrado, no solo el primer par
                if caracter_actual == caracter_apertura:
                    contador += 1
                elif caracter_actual == caracter_cierre:
                    contador -= 1
                posicion += 1
            # Solo retornamos una posición válida si todos los corchetes están
            # balanceados (contador == 0)
            return posicion - 1 if contador == 0 else -1

        # El manejo de IndexError es necesario para casos donde el código
        # termina abruptamente dentro de una expresión con corchetes
        except IndexError:
            return -1

    @staticmethod
    def encontrar_limite_expresion(codigo: str, posicion_inicial: int) -> int:
        """
        Encuentra el límite de una expresión en el código.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición inicial de búsqueda

        Returns:
            int: Posición final de la expresión

        Example:
            >>> encontrar_limite_expresion("x + y, z", 0)
            5
        """
        try:
            posicion = posicion_inicial
            while posicion < len(codigo):
                # Los corchetes/paréntesis de apertura requieren un tratamiento
                # especial, ya que pueden contener expresiones anidadas
                if codigo[posicion] in '([':
                    posicion_coincidente = \
                        AnalizadorCorchetes.encontrar_par_corchetes(
                        codigo,
                        posicion,
                        (codigo[posicion], CORCHETES[codigo[posicion]])
                    )
                    # Si no se encuentra el par, asumimos que la expresión
                    # continúa hasta el final, esto maneja casos de código
                    # malformado sin lanzar excepciones
                    if posicion_coincidente == -1:
                        return len(codigo)
                    posicion = posicion_coincidente + 1
                # Los delimitadores naturales de expresiones incluyen espacios y
                # símbolos de cierre
                elif codigo[posicion] in ' ,)]}\n':
                    return posicion
                posicion += 1
            return len(codigo)
        # El manejo de IndexError es necesario para casos donde el código está
        # truncado o malformado, evitando que el analizador falle
        except IndexError:
            return len(codigo)
