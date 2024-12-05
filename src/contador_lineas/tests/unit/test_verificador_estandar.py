# tests/unit/arbol/test_verificador_estandar_codigo.py
import pytest
from unittest.mock import Mock

from contador_lineas.core.arbol.verificador_estandar_codigo import VerificadorEstandarCodigo
from contador_lineas.core.arbol.nodo import Nodo
from contador_lineas.models.nodos import TipoNodo, InformacionExpresion


class TestVerificadorEstandarCodigo:
    @pytest.fixture
    def verificador(self):
        return VerificadorEstandarCodigo()

    @pytest.fixture
    def crear_nodo(self):
        def _crear_nodo(tipo=TipoNodo.ROOT, contenido="", hijos=None):
            nodo = Nodo(tipo, contenido, 0)
            if hijos:
                for hijo in hijos:
                    nodo.agregar_hijo(hijo)
            return nodo
        return _crear_nodo

    def test_archivo_vacio(self, verificador, crear_nodo):
        raiz = crear_nodo()
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(raiz)
        assert not es_valido
        assert "debe tener al menos una línea" in mensaje

    def test_estructura_vacia(self, verificador, crear_nodo):
        raiz = crear_nodo(TipoNodo.CLASS, "class Test:", [])
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(raiz)
        assert not es_valido
        assert "debe tener contenido" in mensaje

    def test_declaraciones_multiples(self, verificador, crear_nodo):
        nodo = crear_nodo(TipoNodo.EXPRESSION, "x = 1; y = 2")
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        assert not es_valido
        assert "varias declaraciones" in mensaje

    def test_operadores_anidados(self, verificador, crear_nodo, monkeypatch):
        # Mock AnalizadorExpresiones
        mock_analizar = Mock(return_value=InformacionExpresion(
            TipoNodo.TERNARY,
            [InformacionExpresion(TipoNodo.TERNARY, [], 0, 10, "")],
            0, 10, ""
        ))
        monkeypatch.setattr("contador_lineas.core.analizadores.analizador_expresiones.AnalizadorExpresiones.analizar", 
                           mock_analizar)

        nodo = crear_nodo(TipoNodo.TERNARY, "x if y else z if a else b")
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        assert not es_valido
        assert "operadores ternarios" in mensaje

    def test_expresion_lambda(self, verificador, crear_nodo):
        nodo = crear_nodo(TipoNodo.EXPRESSION, "lambda x: x + 1")
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        assert not es_valido
        assert "expresiones lambda" in mensaje

    def test_codigo_valido(self, verificador, crear_nodo):
        raiz = crear_nodo(TipoNodo.ROOT, "", [
            crear_nodo(TipoNodo.CLASS, "class Test:", [
                crear_nodo(TipoNodo.METHOD, "def method(self):", [
                    crear_nodo(TipoNodo.EXPRESSION, "return 42")
                ])
            ])
        ])
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(raiz)
        assert es_valido
        assert mensaje == ""

    def test_comentarios_ignorados(self, verificador, crear_nodo):
        nodo = crear_nodo(TipoNodo.COMMENT, "# x = 1; y = 2")
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        assert es_valido
        assert mensaje == ""

    @pytest.mark.parametrize("contenido,esperado", [
        ("'texto; con punto y coma'", False),
        ('"texto; con punto y coma"', False),
        ("x = 1; y = 2", True),
        ("x = 1; # comentario", False),
        ('x = 1; """docstring"""', True)
    ])
    def test_deteccion_multiples_declaraciones(self, verificador, contenido, esperado):
        assert verificador._tiene_multiples_declaraciones(contenido) == esperado

    def test_manejo_errores(self, verificador, crear_nodo, monkeypatch):
        def mock_validar(*args):
            raise Exception("Error simulado")
        monkeypatch.setattr(verificador, "_validar_nodo", mock_validar)
        
        nodo = crear_nodo()
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        # Agregar aserciones
        assert not es_valido
        assert "Error al validar nodo" in mensaje

    def test_error_analisis_expresiones(self, verificador, crear_nodo, monkeypatch):
        # Mock AnalizadorExpresiones para simular error
        def mock_analizar(*args):
            raise Exception("Error en análisis")
        monkeypatch.setattr("contador_lineas.core.analizadores.analizador_expresiones.AnalizadorExpresiones.analizar", 
                           mock_analizar)

        nodo = crear_nodo(TipoNodo.TERNARY, "x if y else z")
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        assert not es_valido
        assert "Error al validar nodo" in mensaje

    def test_analizador_cadenas_error(self, verificador, crear_nodo, monkeypatch):
        # Mock AnalizadorCadenas para simular error
        def mock_encontrar(*args):
            raise Exception("Error en análisis de cadenas")
        monkeypatch.setattr("contador_lineas.core.analizadores.analizador_cadenas.AnalizadorCadenas.encontrar_sin_comillas",
                           mock_encontrar)

        nodo = crear_nodo(TipoNodo.EXPRESSION, "lambda x: x")
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        assert not es_valido
        assert "Error al validar nodo" in mensaje

    def test_estructura_anidada_compleja(self, verificador, crear_nodo):
        raiz = crear_nodo(TipoNodo.ROOT, "", [
            crear_nodo(TipoNodo.CLASS, "class Test:", [
                crear_nodo(TipoNodo.METHOD, "def method(self):", [
                    crear_nodo(TipoNodo.IF, "if condition:", [
                        crear_nodo(TipoNodo.EXPRESSION, "x = 1"),
                        crear_nodo(TipoNodo.FOR, "for i in range(10):", [
                            crear_nodo(TipoNodo.EXPRESSION, "print(i)")
                        ])
                    ])
                ])
            ])
        ])
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(raiz)
        assert es_valido
        assert mensaje == ""

    def test_docstring_con_punto_y_coma(self, verificador, crear_nodo):
        nodo = crear_nodo(TipoNodo.MODULE_DOCSTRING, '"""Un; docstring;"""')
        es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
        assert es_valido
        assert mensaje == ""

    # Agregar estos métodos de prueba a la clase TestVerificadorEstandarCodigo
    def test_falso_positivo_lambda_en_string(self, verificador, crear_nodo):
        # Casos donde "lambda" aparece en strings/comentarios
        casos = [
            (TipoNodo.EXPRESSION, "'lambda es una palabra'"),
            (TipoNodo.EXPRESSION, '"Función lambda en texto"'),
            (TipoNodo.EXPRESSION, '"""Tutorial sobre lambda"""'),
            (TipoNodo.COMMENT, "# lambda x: x"),
            (TipoNodo.ASSIGNMENT, "variable_lambda = 42"),
            (TipoNodo.EXPRESSION, 'print("lambda")')
        ]
        
        for tipo, contenido in casos:
            nodo = crear_nodo(tipo, contenido)
            es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
            assert es_valido, f"Falló para: {contenido}"
            assert mensaje == "", f"Mensaje inesperado para: {contenido}"

    def test_falso_positivo_operador_ternario_en_string(self, verificador, crear_nodo):
        # Casos donde aparecen operadores ternarios anidados en strings/comentarios
        casos = [
            (TipoNodo.TERNARY, "x if y else '(a if b else c)'"),
            (TipoNodo.EXPRESSION, '"result = value if check else (x if y else z)"'),
            (TipoNodo.EXPRESSION, '"""nested = first if test else (second if other else third)"""'),
            (TipoNodo.COMMENT, "# value if condition else (x if y else z)"),
            (TipoNodo.ASSIGNMENT, "texto = 'result = (a if x else y) if condition else z'"),
            (TipoNodo.EXPRESSION, 'print("output = x if a else (y if b else (z if c else d))")')
        ]
        
        for tipo, contenido in casos:
            nodo = crear_nodo(tipo, contenido)
            es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
            assert es_valido, f"Falló para: {contenido}"
            assert mensaje == "", f"Mensaje inesperado para: {contenido}"

    def test_falso_positivo_comprehension_en_string(self, verificador, crear_nodo):
        # Casos donde aparecen comprehensions anidados en strings/comentarios
        casos = [
            (TipoNodo.EXPRESSION, "'[x for x in [y for y in range(10)]]'"),
            (TipoNodo.EXPRESSION, '"matriz = [[i+j for j in range(3)] for i in range(3)]"'),
            (TipoNodo.EXPRESSION, '"""data = {k:v for k,v in [(x, [y for y in range(x)]) for x in range(5)]}"""'),
            (TipoNodo.COMMENT, "# [f(x) for x in (y for y in range(10))]"),
            (TipoNodo.SET_COMPREHENSION, "ejemplo = {k:'[x for x in v]' for k,v in dict.items()}"),
            (TipoNodo.EXPRESSION, 'print("[x for x in (y for y in [z for z in range(5)])]")')
        ]
        
        for tipo, contenido in casos:
            nodo = crear_nodo(tipo, contenido)
            es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
            assert es_valido, f"Falló para: {contenido}"
            assert mensaje == "", f"Mensaje inesperado para: {contenido}"

    def test_falso_positivo_punto_y_coma_en_string(self, verificador, crear_nodo):
        casos = [
            (TipoNodo.EXPRESSION, "'comando1; comando2'"),
            (TipoNodo.EXPRESSION, '"x=1; y=2"'),
            (TipoNodo.EXPRESSION, '"""a=1; b=2"""'),
            (TipoNodo.COMMENT, "# x=1; y=2"),
            (TipoNodo.EXPRESSION, "texto = 'cmd1; cmd2'")
        ]
        
        for tipo, contenido in casos:
            nodo = crear_nodo(tipo, contenido)
            es_valido, mensaje = verificador.es_arbol_sintactico_valido(nodo)
            assert es_valido, f"Falló para: {contenido}"
            assert mensaje == "", f"Mensaje inesperado para: {contenido}"