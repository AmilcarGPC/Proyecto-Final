# tests/integration/test_analizador.py
import pytest
from pathlib import Path

from contador_lineas.core.contadores.analizador import (
    AnalizadorCodigo, 
    ResultadoAnalisis, 
    ExcepcionAnalizador
)
from contador_lineas.tests.fixtures.estructuras_basicas import *
from contador_lineas.tests.fixtures.casos_evaluacion import CASOS_EVALUACION

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

    def test_archivo_vacio(self, analizador, crear_archivo_temporal):
        archivo = crear_archivo_temporal(ARCHIVO_VACIO)
        with pytest.raises(ExcepcionAnalizador) as excinfo:
            analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        assert "debe tener al menos una línea" in str(excinfo.value)

    def test_archivo_basico(self, analizador, crear_archivo_temporal):
        archivo = crear_archivo_temporal(FUNCION_BASICA)
        resultado = analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        assert isinstance(resultado, ResultadoAnalisis)
        assert resultado.lineas_fisicas == 2
        assert resultado.lineas_logicas == 1
        assert resultado.nombre_archivo == "test.py"

    def test_archivo_complejo(self, analizador, crear_archivo_temporal):
        contenido = """
class Test:
    '''Docstring de clase'''
    def __init__(self):
        self.x = 1
        
    def metodo(self):
        # Comentario
        return [x for x in range(10) if x % 2 == 0]
        
    @property
    def prop(self):
        return self.x * 2
"""
        archivo = crear_archivo_temporal(contenido)
        resultado = analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        assert resultado.lineas_fisicas > 0
        assert resultado.lineas_logicas > 0

    def test_archivo_viola_estandar(self, analizador, crear_archivo_temporal):
        contenido = """
def funcion():
    x = 1; y = 2  # Multiples declaraciones
    return [x for x in [y for y in range(10)]]  # Comprehension anidada
"""
        archivo = crear_archivo_temporal(contenido)
        with pytest.raises(ExcepcionAnalizador) as excinfo:
            analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        assert "Violación del estándar" in str(excinfo.value)

    def test_archivo_invalido(self, analizador):
        with pytest.raises(ExcepcionAnalizador) as excinfo:
            analizador.analizar_archivo("no_existe.py", "no_existe.py", "tests.json")
        assert "Archivo inválido" in str(excinfo.value)

    @pytest.mark.parametrize("caso_nombre, caso_data", CASOS_EVALUACION.items())
    def test_casos_evaluacion(self, analizador, crear_archivo_temporal, caso_nombre, caso_data):
        archivo = crear_archivo_temporal(caso_data['codigo'])
        if caso_data.get('debe_fallar', False):
            with pytest.raises(ExcepcionAnalizador):
                analizador.analizar_archivo(str(archivo), caso_nombre, "tests.json")
        else:
            resultado = analizador.analizar_archivo(str(archivo), caso_nombre, "tests.json")
            assert resultado.lineas_fisicas == caso_data['lineas_fisicas']
            assert resultado.lineas_logicas == caso_data['lineas_logicas']

    def test_estado_interno(self, analizador, crear_archivo_temporal):
        archivo = crear_archivo_temporal(CLASE_CON_METODOS)
        analizador.analizar_archivo(str(archivo), "test.py", "tests.json")
        
        # Verificar que se mantiene el estado interno
        assert analizador.codigo is not None
        assert analizador.arbol is not None
        
        # Verificar que el árbol se construyó correctamente
        assert analizador.arbol.raiz is not None
        assert len(analizador.arbol.raiz.hijos) > 0