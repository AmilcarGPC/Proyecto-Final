# tests/unit/contadores/test_contador_fisico.py
import pytest

from contador_lineas.core.contadores.contador_fisico import ContadorLineasFisicas
from contador_lineas.tests.conftest import crear_arbol_desde_string
from contador_lineas.tests.fixtures.estructuras_basicas import *
from contador_lineas.tests.fixtures.casos_evaluacion import CASOS_EVALUACION


class TestContadorLineasFisicas:
    @pytest.fixture
    def contador(self):
        return ContadorLineasFisicas()

    def test_archivo_vacio(self, contador):
        arbol = crear_arbol_desde_string(ARCHIVO_VACIO)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 0

    def test_solo_blanco(self, contador):
        arbol = crear_arbol_desde_string(SOLO_BLANCO)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 0

    def test_solo_comentarios(self, contador):
        arbol = crear_arbol_desde_string(SOLO_COMENTARIOS)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 0

    def test_solo_docstrings(self, contador):
        arbol = crear_arbol_desde_string(SOLO_DOCSTRINGS)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 0

    def test_importacion_simple(self, contador):
        arbol = crear_arbol_desde_string(IMPORTACION_SIMPLE)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 1
    
    def test_importacion_multiple(self, contador):
        arbol = crear_arbol_desde_string(IMPORTACION_MULTIPLE)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 2

    def test_asignacion_simple(self, contador):
        arbol = crear_arbol_desde_string(ASIGNACION_SIMPLE)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 1
    
    def test_asignacion_multiple(self, contador):
        arbol = crear_arbol_desde_string(ASIGNACION_MULTIPLE)
        assert contador.contar_lineas_fisicas(arbol.raiz) == 3

    @pytest.mark.parametrize("caso_nombre, caso_data", CASOS_EVALUACION.items())
    def test_caso_evaluacion(self, contador, caso_nombre, caso_data):
        arbol = crear_arbol_desde_string(caso_data['codigo'])
        assert contador.contar_lineas_fisicas(arbol.raiz) == caso_data['lineas_fisicas']

