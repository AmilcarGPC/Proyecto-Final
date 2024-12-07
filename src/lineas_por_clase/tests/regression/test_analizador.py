# tests/regression/test_analizador.py
import pytest
from pathlib import Path

from lineas_por_clase.core.contadores.analizador import (
    AnalizadorCodigo,
    ResultadoAnalisis,
    ExcepcionAnalizador
)
from lineas_por_clase.models.metricas import MetricasClase


class TestAnalizadorCodigo:
    @pytest.fixture
    def analizador(self):
        return AnalizadorCodigo()

    @pytest.fixture
    def crear_archivo_temporal(self, tmp_path):
        def _crear_archivo(contenido: str) -> Path:
            archivo = tmp_path / "test.py"
            archivo.write_text(contenido)
            return archivo
        return _crear_archivo

    def test_archivo_basico(self, analizador, crear_archivo_temporal):
        codigo = """
def funcion():
    return 42
        """
        archivo = crear_archivo_temporal(codigo)
        resultado = analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        
        assert isinstance(resultado, ResultadoAnalisis)
        assert resultado.total_lineas_fisicas == 2
        assert len(resultado.clases) == 1  # Solo "otros"
        assert resultado.clases[0].nombre_clase == ""
        assert resultado.nombre_archivo == "test.py"

    def test_archivo_con_clase(self, analizador, crear_archivo_temporal):
        codigo = """
class Ejemplo:
    def __init__(self):
        pass
        
    def metodo(self):
        return True
        """
        archivo = crear_archivo_temporal(codigo)
        resultado = analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        
        assert len(resultado.clases) == 2  # Clase + otros
        clase = next(c for c in resultado.clases if c.nombre_clase == "Ejemplo")
        assert clase.cantidad_metodos == 2
        assert clase.lineas_fisicas == 5
        assert resultado.total_lineas_fisicas == 5

    def test_multiples_clases(self, analizador, crear_archivo_temporal):
        codigo = """
class A:
    def metodo_a(self): 
        pass

class B:
    def metodo_b(self): 
        pass
        """
        archivo = crear_archivo_temporal(codigo)
        resultado = analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        
        assert len(resultado.clases) == 3  # 2 clases + otros
        nombres_clases = {c.nombre_clase for c in resultado.clases}
        assert nombres_clases == {"A", "B", ""}
        assert resultado.total_lineas_fisicas == 6

    def test_codigo_fuera_de_clases(self, analizador, crear_archivo_temporal):
        codigo = """
def funcion_global():
    pass

variable = 42

class Ejemplo:
    pass
        """
        archivo = crear_archivo_temporal(codigo)
        resultado = analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        
        otros = next(c for c in resultado.clases if c.nombre_clase == "")
        assert otros.lineas_fisicas == 3
        assert otros.cantidad_metodos == 0
        assert resultado.total_lineas_fisicas == 5

    def test_archivo_vacio(self, analizador, crear_archivo_temporal):
        codigo = ""  # Archivo vacío con líneas en blanco
        archivo = crear_archivo_temporal(codigo)
        with pytest.raises(ExcepcionAnalizador) as excinfo:
            analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        assert "debe tener al menos una línea" in str(excinfo.value)

    def test_validacion_estandar(self, analizador, crear_archivo_temporal):
        codigo = """
class MalaClase:
    def metodo(self): x = 1; y = 2  # multiples declaraciones
        """
        archivo = crear_archivo_temporal(codigo)
        with pytest.raises(ExcepcionAnalizador) as excinfo:
            analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        assert "Violación del estándar" in str(excinfo.value)

    def test_archivo_invalido(self, analizador):
        with pytest.raises(ExcepcionAnalizador) as excinfo:
            analizador.analizar_archivo("no_existe.py", "no_existe.py", "tests.json")
        assert "Archivo inválido" in str(excinfo.value)