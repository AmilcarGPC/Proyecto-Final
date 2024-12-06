"""
Nombre del módulo: analizador_cadenas.py
Ruta: src/core/analyzers/analizador_cadenas.py
Descripción: Analiza y procesa cadenas de texto en código Python
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - No requiere dependencias externas

Uso:
    from core.analizadores.analizador_cadenas import AnalizadorCadenas
    
    analizador = AnalizadorCadenas()
    esta_en_cadena = analizador.esta_en_cadena(codigo, posicion)

Notas:
    - Procesa caracteres escapados y comillas
    - Maneja comentarios en el código
"""

class AnalizadorCadenas:
    """
    Analizador de cadenas de texto en código Python.

    Procesa y analiza cadenas de texto para identificar comillas,
    caracteres escapados y comentarios.

    Methods:
        esta_en_cadena(codigo: str, posicion: int) -> bool:
            Verifica si una posición está dentro de una cadena.
        encontrar_sin_comillas(codigo: str, subcadena: str, posicion_inicio: \
        int) -> int:
            Encuentra una subcadena fuera de comillas.
        contar_sin_comillas(codigo: str, caracter: str) -> int:
            Cuenta ocurrencias de un caracter fuera de comillas.

    Example:
        >>> analizador = AnalizadorCadenas()
        >>> analizador.esta_en_cadena("'texto'", 2)
        True
    """
    
    @staticmethod
    def esta_en_cadena(
            codigo: str,
            posicion: int,
            cerrado: bool = False) -> bool:
        """
        Verifica si una posición está dentro de una cadena de texto.
        
        Args:
            codigo (str): Código fuente a analizar
            posicion (int): Posición a verificar
            cerrado (bool): Si True, verifica que la cadena esté correctamente \
            cerrada
            
        Returns:
            bool: True si está dentro de comillas (y cerrada si cerrado=True)
        """
        if not cerrado:
            return AnalizadorCadenas._esta_en_cadena_simple(codigo, posicion)
        return AnalizadorCadenas._esta_en_cadena_cerrada(codigo, posicion)
            
    @staticmethod
    def encontrar_sin_comillas(
            codigo: str,
            subcadena: str,
            posicion_inicio: int = 0,
            cerrado: bool = False
        ) -> int:
        """
        Encuentra una subcadena fuera de comillas en el código.

        Args:
            codigo (str): Código fuente a analizar
            subcadena (str): Texto a buscar
            posicion_inicio (int): Posición inicial de búsqueda
            cerrado (bool): Si True, verifica que la cadena esté correctamente \
            cerrada

        Returns:
            int: Posición donde se encuentra la subcadena o -1

        Example:
            >>> encontrar_sin_comillas("x = 'y'", "=", 0)
            2
        """
        posicion = posicion_inicio
        while True:
            posicion = codigo.find(subcadena, posicion)
            if posicion == -1:
                return -1
            if not AnalizadorCadenas.esta_en_cadena(codigo, posicion, cerrado):
                return posicion
            posicion += 1

    @staticmethod
    def contar_sin_comillas(codigo: str, caracter: str) -> int:
        """
        Cuenta ocurrencias de un caracter fuera de comillas.

        Args:
            codigo (str): Código fuente a analizar
            caracter (str): Caracter a contar

        Returns:
            int: Número de ocurrencias encontradas

        Example:
            >>> contar_sin_comillas("x = 'y'", "=")
            1
        """
        contador = 0
        indice = 0
        escapado = False
        
        while indice < len(codigo):
            if codigo[indice] == '\\':
                escapado = not escapado
                indice += 1
                continue
            
            if codigo[indice] == '#':
                break
            
            if not escapado and codigo[indice] in '"\'':
                caracter_comilla = codigo[indice]
                indice_interno = indice + 1
                encontro_par = False
                
                while indice_interno < len(codigo):
                    if codigo[indice_interno] == '\\':
                        indice_interno += 2
                        continue
                    if codigo[indice_interno] == caracter_comilla:
                        encontro_par = True
                        indice = indice_interno + 1
                        break
                    indice_interno += 1
                
                if not encontro_par:
                    if codigo[indice] == caracter:
                        contador += 1
                    indice += 1
            else:
                if codigo[indice] == caracter:
                    contador += 1
                indice += 1
            
            escapado = False
        
        return contador
    
    @staticmethod
    def _esta_en_cadena_simple(codigo: str, posicion: int) -> bool:
        """
        Verifica si una posición está dentro de una cadena simple.

        Args:
            codigo (str): Código fuente a analizar
            posicion (int): Posición a verificar

        Returns:
            bool: True si está dentro de comillas simples
        """
        comilla_simple = False
        comilla_doble = False
        escapado = False
            
        for indice in range(posicion):
            if codigo[indice] == '\\':
                escapado = not escapado
                continue
                
            if not escapado:
                if codigo[indice] == "'":
                    if not comilla_doble:
                        comilla_simple = not comilla_simple
                elif codigo[indice] == '"':
                    if not comilla_simple:
                        comilla_doble = not comilla_doble
            escapado = False
            
        return comilla_simple or comilla_doble
    
    @staticmethod
    def _esta_en_cadena_cerrada(codigo: str, posicion: int) -> bool:
        """
        Verifica si una posición está dentro de una cadena cerrada.

        Args:
            codigo (str): Código fuente a analizar
            posicion (int): Posición a verificar

        Returns:
            bool: True si está dentro de comillas cerradas
        """
        i = posicion - 1
        comilla_apertura = None
        tipo_comilla = None
        escapado = False

        while i >= 0:
            if codigo[i] == '\\':
                escapado = not escapado
                i -= 1
                continue
                
            if not escapado and (codigo[i] == '"' or codigo[i] == "'"):
                temp_pos = i - 1
                temp_escapado = False
                otro_tipo = False
                    
                while temp_pos >= 0:
                    if codigo[temp_pos] == '\\':
                        temp_escapado = not temp_escapado
                        temp_pos -= 1
                        continue
                        
                    if not temp_escapado:
                        if codigo[temp_pos] == ('"' if codigo[i] == "'" else \
                        "'"):
                            otro_tipo = True
                            break
                    temp_escapado = False
                    temp_pos -= 1
                    
                if not otro_tipo:
                    comilla_apertura = i
                    tipo_comilla = codigo[i]
                    break
                        
            escapado = False
            i -= 1

        if comilla_apertura is None:
            return False

        i = posicion + 1
        escapado = False
            
        while i < len(codigo):
            if codigo[i] == '\\':
                escapado = not escapado
                i += 1
                continue
                    
            if not escapado and codigo[i] == tipo_comilla:
                return True
                    
            escapado = False
            i += 1

        return False
