"""
Nombre del módulo: analizador_corchetes.py
Ruta: src/core/analyzers/analizador_corchetes.py
Descripción: Analiza y encuentra pares de corchetes y límites de expresiones en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18/11/2024
Última Actualización: 18/11/2024

Dependencias:
    - core.constantes.CORCHETES

Uso:
    from config.analizador_corchetes import AnalizadorCorchetes
    
    analizador = AnalizadorCorchetes()
    posicion = analizador.encontrar_par_corchetes(codigo, pos_inicial, ('(', ')'))

Notas:
    - Maneja paréntesis [] y ()
    - Retorna -1 si no encuentra el par correspondiente
"""
from core.constantes import CORCHETES


class AnalizadorCorchetes:
    """
    Analizador de corchetes y expresiones en código Python.

    Proporciona funcionalidad para encontrar pares de corchetes correspondientes
    y límites de expresiones en código fuente Python.

    Methods:
        encontrar_par_corchetes(codigo: str, posicion_inicial: int, corchetes: tuple[str, str]) -> int:
            Encuentra la posición del corchete de cierre correspondiente.
        encontrar_limite_expresion(codigo: str, posicion_inicial: int) -> int:
            Encuentra el límite de una expresión en el código.

    Example:
        >>> analizador = AnalizadorCorchetes()
        >>> analizador.encontrar_par_corchetes("(x + y)", 0, ('(', ')'))
        6
    """
    @staticmethod
    def encontrar_par_corchetes(codigo: str, posicion_inicial: int, corchetes: tuple[str, str]) -> int:
        """
        Encuentra la posición del corchete de cierre correspondiente.

        Args:
            codigo (str): Código fuente a analizar
            posicion_inicial (int): Posición del corchete de apertura
            corchetes (tuple[str, str]): Par de caracteres de apertura y cierre

        Returns:
            int: Posición del corchete de cierre o -1 si no se encuentra

        Example:
            >>> encontrar_par_corchetes("(x + y)", 0, ('(', ')'))
            6
        """
        try:
            caracter_apertura, caracter_cierre = corchetes
            contador = 1
            posicion = posicion_inicial + 1
            
            while posicion < len(codigo) and contador > 0:
                caracter_actual = codigo[posicion]
                if caracter_actual == caracter_apertura:
                    contador += 1
                elif caracter_actual == caracter_cierre:
                    contador -= 1
                posicion += 1
                
            return posicion - 1 if contador == 0 else -1
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
                if codigo[posicion] in '([':
                    posicion_coincidente = AnalizadorCorchetes.encontrar_par_corchetes(
                        codigo, 
                        posicion,
                        (codigo[posicion], CORCHETES[codigo[posicion]])
                    )
                    if posicion_coincidente == -1:
                        return len(codigo)
                    posicion = posicion_coincidente + 1
                elif codigo[posicion] in ' ,)]}\n':
                    return posicion
                posicion += 1
            return len(codigo)
        except IndexError:
            return len(codigo)