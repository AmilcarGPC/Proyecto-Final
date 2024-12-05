# tests/unit/utils/test_archivo_utils.py
import pytest

from pathlib import Path

from contador_lineas.utils.archivo_utils import (
    leer_archivo_texto,
    leer_json,
    escribir_json,
    escribir_python
)
from contador_lineas.tests.fixtures.json_metricas import METRICAS_REGISTRO


class TestLeerArchivoTexto:
    @pytest.fixture
    def crear_archivo_temporal(self, tmp_path):
        def _crear_archivo(contenido, encoding='utf-8'):
            archivo = tmp_path / "test.txt"
            archivo.write_text(contenido, encoding=encoding)
            return archivo
        return _crear_archivo

    def test_archivo_vacio(self, crear_archivo_temporal):
        archivo = crear_archivo_temporal("")
        lineas, error = leer_archivo_texto(archivo)
        assert lineas == []
        assert error is None

    def test_archivo_simple(self, crear_archivo_temporal):
        contenido = "línea1\nlínea2\n"
        archivo = crear_archivo_temporal(contenido)
        lineas, error = leer_archivo_texto(archivo)
        assert lineas == ["línea1\n", "línea2\n"]
        assert error is None

    def test_codificacion_invalida(self, crear_archivo_temporal):
        contenido = "áéíóú"
        archivo = crear_archivo_temporal(contenido, 'utf-8')
        lineas, error = leer_archivo_texto(archivo, 'ascii')
        assert lineas == []
        assert "Error de codificación" in error

    def test_archivo_no_existe(self):
        lineas, error = leer_archivo_texto("archivo_no_existe.txt")
        assert lineas == []
        assert "Error al leer el archivo" in error

class TestLeerEscribirJson:
    @pytest.fixture
    def crear_json_temporal(self, tmp_path):
        def _crear_json(datos):
            archivo = tmp_path / "tests.json"
            escribir_json(archivo, datos)
            return archivo
        return _crear_json

    def test_metricas_archivo_simple(self, crear_json_temporal):
        datos_originales = {
            "test_1.py": {
                "nombre_archivo": "test_1.py",
                "lineas_logicas": 35,
                "lineas_fisicas": 92
            }
        }
        archivo = crear_json_temporal(datos_originales)
        datos_leidos = leer_json(archivo)
        assert datos_leidos == datos_originales

    def test_metricas_multiple_archivos(self, crear_json_temporal):
        archivo = crear_json_temporal(METRICAS_REGISTRO)
        datos_leidos = leer_json(archivo)
        assert datos_leidos == METRICAS_REGISTRO
        assert len(datos_leidos) == 3
        assert all(
            "lineas_logicas" in datos_leidos[archivo] 
            for archivo in datos_leidos
        )

    def test_json_vacio(self, crear_json_temporal):
        datos_originales = {}
        archivo = crear_json_temporal(datos_originales)
        datos_leidos = leer_json(archivo)
        assert datos_leidos == datos_originales

    def test_json_no_existe(self):
        with pytest.raises(Exception):
            leer_json("archivo_no_existe.json")

class TestEscribirPython:
    @pytest.fixture
    def archivo_temporal(self, tmp_path):
        return tmp_path / "test.py"

    def test_escribir_vacio(self, archivo_temporal):
        error = escribir_python(archivo_temporal, [])
        assert error is None
        assert archivo_temporal.read_text() == ""

    def test_escribir_con_saltos(self, archivo_temporal):
        lineas = ["def suma(a, b):\n", "    return a + b\n", "\n"]
        error = escribir_python(archivo_temporal, lineas)
        assert error is None
        assert archivo_temporal.read_text() == "def suma(a, b):\n    return a + b\n\n"

    def test_escribir_sin_saltos(self, archivo_temporal):
        lineas = ["x = 1", "y = 2"]
        error = escribir_python(archivo_temporal, lineas)
        assert error is None
        assert archivo_temporal.read_text() == "x = 1\ny = 2\n"

    def test_error_permisos(self, monkeypatch):
        def mock_open(*args, **kwargs):
            raise PermissionError("Sin permisos")
        monkeypatch.setattr("builtins.open", mock_open)
        
        error = escribir_python("test.py", ["x = 1"])
        assert "Error al escribir el archivo" in error