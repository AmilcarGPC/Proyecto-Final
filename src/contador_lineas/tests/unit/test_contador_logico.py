# tests/unit/contadores/test_contador_logico.py
import pytest

from contador_lineas.core.contadores.contador_logico import ContadorLineasLogicas
from contador_lineas.tests.conftest import crear_arbol_desde_string
from contador_lineas.tests.fixtures.estructuras_basicas import *
from contador_lineas.tests.fixtures.casos_evaluacion import CASOS_EVALUACION


class TestContadorLineasLogicas:
    @pytest.fixture
    def contador(self):
        return ContadorLineasLogicas()

    def test_archivo_vacio(self, contador):
        arbol = crear_arbol_desde_string(ARCHIVO_VACIO)
        assert contador.contar_lineas_logicas(arbol.raiz) == 0

    def test_solo_blanco(self, contador):
        arbol = crear_arbol_desde_string(SOLO_BLANCO)
        assert contador.contar_lineas_logicas(arbol.raiz) == 0

    def test_solo_comentarios(self, contador):
        arbol = crear_arbol_desde_string(SOLO_COMENTARIOS)
        assert contador.contar_lineas_logicas(arbol.raiz) == 0

    def test_solo_docstrings(self, contador):
        arbol = crear_arbol_desde_string(SOLO_DOCSTRINGS)
        assert contador.contar_lineas_logicas(arbol.raiz) == 0

    def test_funcion_basica(self, contador):
        arbol = crear_arbol_desde_string(FUNCION_BASICA)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1
    
    def test_funcion_con_parametros(self, contador):
        arbol = crear_arbol_desde_string(FUNCION_CON_PARAMETROS)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_funcion_con_parametros_y_docstring(self, contador):
        arbol = crear_arbol_desde_string(FUNCION_CON_PARAMETROS_Y_DOCSTRING)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_clase_basica(self, contador):
        arbol = crear_arbol_desde_string(CLASE_BASICA)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_clase_con_metodos(self, contador):
        arbol = crear_arbol_desde_string(CLASE_CON_METODOS)
        assert contador.contar_lineas_logicas(arbol.raiz) == 4

    def test_clase_con_metodos_y_docstring(self, contador):
        arbol = crear_arbol_desde_string(CLASE_CON_METODOS_Y_DOCSTRING)
        assert contador.contar_lineas_logicas(arbol.raiz) == 4

    def test_if_elif_else(self, contador):
        arbol = crear_arbol_desde_string(IF_ELIF_ELSE)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1
    
    def test_for(self, contador):
        arbol = crear_arbol_desde_string(FOR)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1
    
    def test_while(self, contador):
        arbol = crear_arbol_desde_string(WHILE)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_match_case(self, contador):
        arbol = crear_arbol_desde_string(MATCH)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_list_comprehension(self, contador):
        arbol = crear_arbol_desde_string(LIST_COMPREHENSION)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1
    
    def test_dict_comprehension(self, contador):
        arbol = crear_arbol_desde_string(DICT_COMPREHENSION)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_set_comprehension(self, contador):
        arbol = crear_arbol_desde_string(SET_COMPREHENSION)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_generador(self, contador):
        arbol = crear_arbol_desde_string(GENERATOR_EXPRESSION)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_ternario(self, contador):
        arbol = crear_arbol_desde_string(TERNARY)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1

    def test_with(self, contador):
        arbol = crear_arbol_desde_string(WITH)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1
    
    def test_try_except_finally(self, contador):
        arbol = crear_arbol_desde_string(TRY_EXCEPT_FINALLY)
        assert contador.contar_lineas_logicas(arbol.raiz) == 1
    
    def test_property(self, contador):
        arbol = crear_arbol_desde_string(PROPERTY)
        assert contador.contar_lineas_logicas(arbol.raiz) == 2

    def test_decorator(self, contador):
        arbol = crear_arbol_desde_string(DECORATOR)
        assert contador.contar_lineas_logicas(arbol.raiz) == 2
    
    @pytest.mark.parametrize("caso_nombre, caso_data", CASOS_EVALUACION.items())
    def test_caso_evaluacion(self, contador, caso_nombre, caso_data):
        arbol = crear_arbol_desde_string(caso_data['codigo'])
        assert contador.contar_lineas_logicas(arbol.raiz) == caso_data['lineas_logicas']
