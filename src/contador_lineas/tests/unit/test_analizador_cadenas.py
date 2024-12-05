# tests/unit/analizadores/test_analizador_cadenas.py
import pytest

from contador_lineas.core.analizadores.analizador_cadenas import AnalizadorCadenas
from contador_lineas.tests.fixtures.cadenas_basicas import *
from contador_lineas.tests.fixtures.cadenas_evaluacion import *


class TestEstaEnCadenaBasico:
    @pytest.fixture
    def analizador(self):
        return AnalizadorCadenas()

    def test_cadena_vacia(self, analizador):
        assert not analizador.esta_en_cadena(CADENA_VACIA, 0)
    
    def test_cadena_simple(self, analizador):
        assert analizador.esta_en_cadena(CADENA_SIMPLE, 2)
        assert not analizador.esta_en_cadena(CADENA_SIMPLE, 0)
        assert analizador.esta_en_cadena(CADENA_SIMPLE, 6)

    def test_cadena_doble(self, analizador):
        assert analizador.esta_en_cadena(CADENA_DOBLE, 2)
        assert not analizador.esta_en_cadena(CADENA_DOBLE, 0)
        assert analizador.esta_en_cadena(CADENA_DOBLE, 6)


class TestEstaEnCadenaAvanzado:
    @pytest.fixture
    def analizador(self):
        return AnalizadorCadenas()

    def test_cadenas_anidadas(self, analizador):
        assert analizador.esta_en_cadena(CADENA_ANIDADA, 15)
        assert analizador.esta_en_cadena(CADENA_ANIDADA, 10)

    def test_cadena_con_escape(self, analizador):
        assert analizador.esta_en_cadena(CADENA_ESCAPE, 12)
        assert not analizador.esta_en_cadena(CADENA_ESCAPE, 0)

    def test_cadena_multilinea(self, analizador):
        assert analizador.esta_en_cadena(CADENA_MULTILINEA, 15)
        assert not analizador.esta_en_cadena(CADENA_MULTILINEA, 0)


class TestEstaEnCadenaCerrada:
    @pytest.fixture
    def analizador(self):
        return AnalizadorCadenas()

    def test_cadenas_multilinea_cerrado(self, analizador):
        assert analizador.esta_en_cadena(CADENA_MULTILINEA_SIN_CERRAR, 10, False)
        assert not analizador.esta_en_cadena(CADENA_MULTILINEA_SIN_CERRAR, 10, True)

    def test_escape_cerrado(self, analizador):
        assert analizador.esta_en_cadena(CADENA_ESCAPE_CERRADA, 12, False)
        assert analizador.esta_en_cadena(CADENA_ESCAPE_CERRADA, 12, True)

    @pytest.mark.parametrize("caso", CASOS_CADENAS_CERRADAS)
    def test_casos_cadenas_cerradas(self, analizador, caso):
        assert analizador.esta_en_cadena(
            caso['codigo'],
            caso['posicion'],
            False
        ) == caso['esperado_simple']
        
        assert analizador.esta_en_cadena(
            caso['codigo'],
            caso['posicion'],
            True
        ) == caso['esperado_cerrado']


class TestEncontrarSinComillas:
    @pytest.fixture
    def analizador(self):
        return AnalizadorCadenas()

    def test_encontrar_basico(self, analizador):
        assert analizador.encontrar_sin_comillas(CADENA_ENCONTRAR_BASICA, "=", 0) == 2
        assert analizador.encontrar_sin_comillas(CADENA_ENCONTRAR_BASICA, "=", 3) == 25

    @pytest.mark.parametrize("caso", CASOS_ENCONTRAR)
    def test_casos_encontrar(self, analizador, caso):
        assert analizador.encontrar_sin_comillas(
            caso['codigo'],
            caso['buscar'],
            caso['inicio']
        ) == caso['esperado_simple']
        
        assert analizador.encontrar_sin_comillas(
            caso['codigo'],
            caso['buscar'],
            caso['inicio'],
            caso['cerrado']
        ) == caso['esperado_cerrado']


class TestContarSinComillas:
    @pytest.fixture
    def analizador(self):
        return AnalizadorCadenas()

    def test_contar_basico(self, analizador):
        assert analizador.contar_sin_comillas(CADENA_CONTAR_BASICA, "=") == 1

    @pytest.mark.parametrize("caso", CASOS_CONTAR)
    def test_casos_contar(self, analizador, caso):
        assert analizador.contar_sin_comillas(
            caso['codigo'],
            caso['caracter']
        ) == caso['esperado']