"""
Nombre del módulo: analizador.py
Ruta: src/core/analizador.py
Descripción: Analiza archivos Python para obtener métricas de líneas de código
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 18-11-2024
Última Actualización: 18-11-2024

Dependencias:
    - core.contadores.contador_fisico.ContadorLineasFisicas
    - core.contadores.contador_logico.ContadorLineasLogicas
    - core.gestion_archivos.lector_archivo.LectorArchivoPython
    - core.gestion_archivos.manejador_json.AlmacenamientoMetricas
    - core.arbol_sintaxis.arbol_archivo.ArbolArchivoPython
    - models.metricas.MetricasArchivo
    - utils.formateador_linea.FormateadorLinea

Uso:
    from core.analizador import Analizador
    
    analizador = Analizador()
    resultado = analizador.analizar_archivo("script.py", "script.py")

Notas:
    - Procesa solo archivos Python válidos
    - Retorna métricas de líneas físicas y lógicas
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from analizador_cambios.core.arbol.nodo import Nodo # AGREGADA TOTALMENTE NUEVA
from analizador_cambios.core.contadores.contador_fisico import (
    ContadorLineasFisicas
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.9% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.contadores.contador_logico import (
    ContadorLineasLogicas
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.9% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.gestion_archivos.lector_archivo import (
    LectorArchivoPython
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.91% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.gestion_archivos.almacenamiento_metricas import (
    AlmacenamientoMetricas
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.92% (las 3 líneas previas cuentan como 1)
from analizador_cambios.core.arbol.arbol_sintactico import ArbolArchivoPython # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.89%
from analizador_cambios.core.arbol.verificador_estandar_codigo import (
    VerificadorEstandarCodigo
) # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.91% (las 3 líneas previas cuentan como 1)
from analizador_cambios.models.metricas import MetricasClase, MetricasArchivo # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.76%
from analizador_cambios.utils.formateador_linea import FormateadorLinea # AGREGADA TOTALMENTE NUEVA


class ExcepcionAnalizador(Exception):
    """
    Excepción personalizada para errores del analizador.

    Se lanza cuando hay errores en el proceso de análisis
    de archivos Python.

    Example:
        >>> raise ExcepcionAnalizador("Archivo inválido")
    """

    pass


@dataclass
class ResultadoAnalisis:
    """
    Almacena el resultado del análisis de un archivo.

    Contiene el conteo de líneas físicas y lógicas junto
    con el nombre del archivo analizado.

    Attributes:
        lineas_fisicas (int): Número de líneas físicas
        lineas_logicas (int): Número de líneas lógicas
        nombre_archivo (str): Nombre del archivo analizado

    Example:
        >>> resultado = ResultadoAnalisis(10, 8, "script.py")
    """

    lineas_fisicas: int
    lineas_logicas: int
    nombre_archivo: str


class AnalizadorCodigo:
    """
    Analiza archivos Python para obtener métricas.

    Procesa archivos fuente Python para obtener conteos de
    líneas físicas y lógicas.

    Attributes:
        almacenamiento (AlmacenamientoMetricas): Gestor de almacenamiento
        formateador (FormateadorLinea): Formateador de líneas
        contador_fisico (ContadorLineasFisicas): Contador de líneas físicas
        contador_logico (ContadorLineasLogicas): Contador de líneas lógicas

    Methods:
        analizar_archivo(ruta_archivo: str, 
            nombre_archivo: str) -> ResultadoAnalisis:
            Analiza un archivo Python y retorna sus métricas.

    Example:
        >>> analizador = Analizador()
        >>> resultado = analizador.analizar_archivo("script.py", "script.py")
    """
    
    def __init__(self):
        self.arbol = None
        self.codigo = None
        self.almacenamiento = AlmacenamientoMetricas()
        self.formateador = FormateadorLinea() # AGREGADA TOTALMENTE NUEVA
        self.contador_fisico = ContadorLineasFisicas()
        self.contador_logico = ContadorLineasLogicas()
        self.verificador_estandar = VerificadorEstandarCodigo()

    def formatear_codigo(self, codigo: list[str]) -> list[str]: # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        Formatea el código fuente para su análisis. # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Args: # AGREGADA TOTALMENTE NUEVA
            codigo (list[str]): Líneas de código a formatear # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Returns: # AGREGADA TOTALMENTE NUEVA
            list[str]: Líneas formateadas # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Example: # AGREGADA TOTALMENTE NUEVA
            >>> formatear_codigo(["def f():", "    pass"]) # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        codigo_nuevo = [] # AGREGADA TOTALMENTE NUEVA
        for linea in codigo: # AGREGADA TOTALMENTE NUEVA
            formateada = self.formateador.formatear_linea(linea) # AGREGADA TOTALMENTE NUEVA
            if len(formateada) > 1: # AGREGADA TOTALMENTE NUEVA
                codigo_nuevo.extend(formateada) # AGREGADA TOTALMENTE NUEVA
            else: # AGREGADA TOTALMENTE NUEVA
                codigo_nuevo.extend(formateada) # AGREGADA TOTALMENTE NUEVA
        return codigo_nuevo # AGREGADA TOTALMENTE NUEVA

    def validate_syntax_tree(
            self, tree: ArbolArchivoPython) -> Tuple[bool, Optional[str]]:
        """
        Valida la estructura sintáctica del AST.

        Args:
            arbol (ArbolArchivoPython): Árbol a validar

        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)

        Example:
            >>> validar_arbol_sintaxis(arbol)
        """
        return self.verificador_estandar.es_arbol_sintactico_valido(tree.raiz)

    def analizar_archivo(
            self, ruta_archivo: str, nombre_archivo: str) -> ResultadoAnalisis:
        """
        Analiza un archivo Python y obtiene sus métricas.

        Args:
            ruta_archivo (str): Ruta al archivo
            nombre_archivo (str): Nombre del archivo

        Returns:
            ResultadoAnalisis: Métricas del archivo

        Example:
            >>> analizar_archivo("script.py", "script.py")
        """
        self._validar_archivo(ruta_archivo)
        codigo = self._obtener_codigo(ruta_archivo)
        self.codigo = codigo
        metricas = self._procesar_codigo(codigo, nombre_archivo)
        self.almacenamiento.guardar_metricas(metricas)
        return self._crear_resultado(metricas)

    def _validar_archivo(self, ruta_archivo: str) -> None:
        """
        Valida que el archivo exista y sea un archivo Python válido.

        Args:
            ruta_archivo (str): Ruta al archivo a validar

        Raises:
            ExcepcionAnalizador: Si el archivo no existe o es inválido

        Example:
            >>> self._validar_archivo("script.py")
        """
        lector = LectorArchivoPython(ruta_archivo)
        es_valido, error = lector.validar()
        if not es_valido:
            raise ExcepcionAnalizador(f"Archivo inválido: {error}")

    def _obtener_codigo(self, ruta_archivo: str) -> list[str]:
        """
        Lee y formatea el código fuente del archivo.

        Args:
            ruta_archivo (str): Ruta al archivo a leer

        Returns:
            list[str]: Lista de líneas de código formateadas

        Example:
            >>> codigo = self._obtener_codigo("script.py")
        """
        lector = LectorArchivoPython(ruta_archivo)
        codigo, error = lector.leer_lineas()
        if error:
            raise ExcepcionAnalizador(f"Error al leer archivo: {error}")
        return self.formatear_codigo(codigo) # AGREGADA TOTALMENTE NUEVA

    def _procesar_codigo(
            self, codigo: list[str], nombre_archivo: str
        ) -> MetricasArchivo:
        """
        Procesa el código y calcula sus métricas.

        Args:
            codigo (list[str]): Líneas de código a procesar
            nombre_archivo (str): Nombre del archivo procesado

        Returns:
            MetricasArchivo: Métricas calculadas del código

        Example:
            >>> metricas = self._procesar_codigo(codigo, "script.py")
        """
        arbol = ArbolArchivoPython(codigo)
        self._validar_arbol_sintaxis(arbol)
        self.arbol = arbol

        clases = self._analizar_clases(arbol) # AGREGADA TOTALMENTE NUEVA
        
        return MetricasArchivo(
            nombre_archivo=nombre_archivo,
            clases=clases
        ) # AGREGADA TOTALMENTE NUEVA (las 4 líneas previas cuentan como 1)
    
    def _analizar_clases(
            self,
            arbol: ArbolArchivoPython) -> list[MetricasClase]: # AGREGADA TOTALMENTE NUEVA (las 3 líneas previas cuentan como 1)
        """ # AGREGADA TOTALMENTE NUEVA
        Analiza las clases de un archivo Python y obtiene métricas. # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Args: # AGREGADA TOTALMENTE NUEVA
            arbol (ArbolArchivoPython): Árbol sintáctico del archivo # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Returns: # AGREGADA TOTALMENTE NUEVA
            list[MetricasClase]: Métricas de las clases del archivo # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Example: # AGREGADA TOTALMENTE NUEVA
            >>> clases = self._analizar_clases(arbol) # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        clases = [] # AGREGADA TOTALMENTE NUEVA
        for nodo in arbol.obtener_nodos_clase(): # AGREGADA TOTALMENTE NUEVA
            metricas_clase = self._analizar_clase(nodo) # AGREGADA TOTALMENTE NUEVA
            clases.append(metricas_clase) # AGREGADA TOTALMENTE NUEVA
        nodo_otros = arbol.obtener_nodo_otros() # AGREGADA TOTALMENTE NUEVA
        otros = self._analizar_clase(nodo_otros) # AGREGADA TOTALMENTE NUEVA
        otros.cantidad_metodos = 0 # AGREGADA TOTALMENTE NUEVA
        otros.lineas_fisicas -= 1 # Restar la línea de la clase # AGREGADA TOTALMENTE NUEVA
        clases.append(otros) # AGREGADA TOTALMENTE NUEVA
        return clases # AGREGADA TOTALMENTE NUEVA
    
    def _analizar_clase(self, clase: Nodo) -> MetricasClase: # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        Analiza una clase Python y obtiene métricas. # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Args: # AGREGADA TOTALMENTE NUEVA
            clase (Nodo): Nodo de la clase a analizar # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Returns: # AGREGADA TOTALMENTE NUEVA
            MetricasClase: Métricas de la clase # AGREGADA TOTALMENTE NUEVA
 # AGREGADA TOTALMENTE NUEVA
        Example: # AGREGADA TOTALMENTE NUEVA
            >>> metricas_clase = self._analizar_clase(clase) # AGREGADA TOTALMENTE NUEVA
        """ # AGREGADA TOTALMENTE NUEVA
        return MetricasClase(
            nombre_clase=clase.obtener_nombre_clase(),
            cantidad_metodos=len(self.arbol.obtener_nodos_metodos(clase)),
            lineas_fisicas=self.contador_fisico.contar_lineas_fisicas(clase)) # AGREGADA TOTALMENTE NUEVA (las 4 líneas previas cuentan como 1)

    def _validar_arbol_sintaxis(self, arbol: ArbolArchivoPython) -> None:
        """
        Valida la estructura sintáctica del AST con respecto al estándar de \
        codificación.

        Args:
            arbol (ArbolArchivoPython): Árbol sintáctico a validar

        Raises:
            ExcepcionAnalizador: Si el árbol tiene errores sintácticos

        Example:
            >>> self._validar_arbol_sintaxis(arbol)
        """
        es_valido, error = self.verificador_estandar.es_arbol_sintactico_valido(
            arbol.raiz
        )
        if not es_valido:
            raise ExcepcionAnalizador(f"Violación del estándar: {error}")

    def _crear_resultado(self, metricas: MetricasArchivo) -> ResultadoAnalisis:
        """
        Crea un objeto ResultadoAnalisis desde las métricas.

        Args:
            metricas (MetricasArchivo): Métricas calculadas

        Returns:
            ResultadoAnalisis: Objeto con el resultado del análisis

        Example:
            >>> resultado = self._crear_resultado(metricas)
        """
        return None # AGREGADA TOTALMENTE NUEVA
