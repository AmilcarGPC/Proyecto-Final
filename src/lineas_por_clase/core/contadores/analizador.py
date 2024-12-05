"""
Nombre del módulo: analizador.py
Ruta: lineas_por_clase/core/contadores/analizador.py
Descripción: Analiza archivos Python para obtener métricas de líneas de código
Proyecto: Sistema de Conteo de Líneas Físicas y Lógicas en Python
Autor: Amílcar Pérez
Organización: Equipo 3
Licencia: MIT
Fecha de Creación: 27-11-2024
Última Actualización: 28-11-2024

Dependencias:
    - core.contadores.contador_fisico.ContadorLineasFisicas
    - core.contadores.contador_logico.ContadorLineasLogicas
    - core.gestion_archivos.lector_archivo.LectorArchivoPython
    - core.gestion_archivos.manejador_json.AlmacenamientoMetricas
    - core.arbol_sintaxis.arbol_archivo.ArbolArchivoPython
    - models.metricas.MetricasArchivo
    - utils.formateador_linea.FormateadorLinea

Uso:
    from lineas_por_clase.core.contadores.analizador import Analizador
    
    analizador = Analizador()
    resultado = analizador.analizar_archivo("script.py", "script.py")

Notas:
    - Procesa solo archivos Python válidos
    - Retorna métricas de líneas físicas y lógicas
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List

from contador_lineas.core.contadores.contador_fisico import (
    ContadorLineasFisicas
)
from contador_lineas.core.gestion_archivos.lector_archivo import (
    LectorArchivoPython
)
from contador_lineas.core.arbol.verificador_estandar_codigo import (
    VerificadorEstandarCodigo
)
from lineas_por_clase.core.arbol.arbol_sintactico import ArbolArchivoPython
from lineas_por_clase.core.arbol.nodo import Nodo
from lineas_por_clase.core.gestion_archivos.almacenamiento_metricas import (
    AlmacenamientoMetricas
)
from lineas_por_clase.models.metricas import MetricasClase, MetricasArchivo


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
        self.contador_fisico = ContadorLineasFisicas()
        self.verificador_estandar = VerificadorEstandarCodigo()

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
            self, 
            ruta_archivo: str,
            nombre_archivo: str,
            ruta_almacenamiento: str = "db/lineas_por_clase_registro.json"
        ) -> ResultadoAnalisis:
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
        # El flujo de análisis sigue un orden específico para garantizar la
        # validez del código antes de procesar y almacenar métricas
        self._validar_archivo(ruta_archivo)
        codigo = self._obtener_codigo(ruta_archivo)
        self.codigo = codigo
        metricas = self._procesar_codigo(codigo, nombre_archivo)
        AlmacenamientoMetricas(ruta_almacenamiento).guardar_metricas(metricas)
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
        # La validación se hace antes de cualquier procesamiento para fallar
        # rápido y evitar cálculos innecesarios
        lector = LectorArchivoPython(ruta_archivo)
        es_valido, error = lector.validar()
        if not es_valido:
            raise ExcepcionAnalizador(f"Archivo inválido: {error}")

    def _obtener_codigo(self, ruta_archivo: str) -> List[str]:
        """
        Lee y formatea el código fuente del archivo.

        Args:
            ruta_archivo (str): Ruta al archivo a leer

        Returns:
            List[str]: Lista de líneas de código formateadas

        Example:
            >>> codigo = self._obtener_codigo("script.py")
        """
        lector = LectorArchivoPython(ruta_archivo)
        codigo, error = lector.leer_lineas()
        if error:
            raise ExcepcionAnalizador(f"Error al leer archivo: {error}")
        return codigo

    def _procesar_codigo(
            self, codigo: List[str], nombre_archivo: str
        ) -> MetricasArchivo:
        """
        Procesa el código y calcula sus métricas.

        Args:
            codigo (List[str]): Líneas de código a procesar
            nombre_archivo (str): Nombre del archivo procesado

        Returns:
            MetricasArchivo: Métricas calculadas del código

        Example:
            >>> metricas = self._procesar_codigo(codigo, "script.py")
        """
        # Construimos y validamos el AST primero para asegurar que el código
        # cumple con el estándar antes de calcular métricas
        arbol = ArbolArchivoPython(codigo)
        self._validar_arbol_sintaxis(arbol)
        self.arbol = arbol

        # Obtenemos las métricas de las clases y otros nodos del archivo
        clases = self._analizar_clases(arbol)

        return MetricasArchivo(
            nombre_archivo=nombre_archivo,
            clases=clases
        )

    def _analizar_clases(
            self,
            arbol: ArbolArchivoPython) -> List[MetricasClase]:
        """
        Analiza las clases de un archivo Python y obtiene métricas.

        Args:
            arbol (ArbolArchivoPython): Árbol sintáctico del archivo

        Returns:
            List[MetricasClase]: Métricas de las clases del archivo

        Example:
            >>> clases = self._analizar_clases(arbol)
        """
        clases = []
        for nodo in arbol.obtener_nodos_clase():
            metricas_clase = self._analizar_clase(nodo)
            clases.append(metricas_clase)
        nodo_otros = arbol.obtener_nodo_otros()
        otros = self._analizar_clase(nodo_otros)
        otros.cantidad_metodos = 0
        otros.lineas_fisicas -= 1 # Restar la línea de la clase
        clases.append(otros)
        return clases

    def _analizar_clase(self, clase: Nodo) -> MetricasClase:
        """
        Analiza una clase Python y obtiene métricas.

        Args:
            clase (Nodo): Nodo de la clase a analizar

        Returns:
            MetricasClase: Métricas de la clase

        Example:
            >>> metricas_clase = self._analizar_clase(clase)
        """
        return MetricasClase(
            nombre_clase=clase.obtener_nombre_clase(),
            cantidad_metodos=len(self.arbol.obtener_nodos_metodos(clase)),
            lineas_fisicas=self.contador_fisico.contar_lineas_fisicas(clase))

    def _validar_arbol_sintaxis(self, arbol: ArbolArchivoPython) -> None:
        """
        Valida la estructura sintáctica del AST con respecto al estándar de 
        codificación.

        Args:
            arbol (ArbolArchivoPython): Árbol sintáctico a validar

        Raises:
            ExcepcionAnalizador: Si el árbol tiene errores sintácticos

        Example:
            >>> self._validar_arbol_sintaxis(arbol)
        """
        es_valido, error = \
        self.verificador_estandar.es_arbol_sintactico_valido(arbol.raiz)
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
        return None
