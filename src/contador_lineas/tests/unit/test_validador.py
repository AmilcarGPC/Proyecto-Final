# tests/unit/utils/test_validador.py
import pytest

from pathlib import Path
from contador_lineas.utils.validador import validar_archivo_python


class TestValidadorArchivoPython:
    @pytest.fixture
    def crear_archivo_temporal(self, tmp_path):
        def _crear_archivo(extension='.py', contenido=''):
            archivo = tmp_path / f"test{extension}"
            archivo.write_text(contenido)
            return archivo
        return _crear_archivo

    def test_archivo_python_valido(self, crear_archivo_temporal):
        archivo = crear_archivo_temporal()
        es_valido, error = validar_archivo_python(archivo)
        assert es_valido
        assert error == ""

    def test_archivo_no_existe(self):
        es_valido, error = validar_archivo_python("no_existe.py")
        assert not es_valido
        assert "no fue encontrado" in error

    def test_extension_incorrecta(self, crear_archivo_temporal):
        archivo = crear_archivo_temporal('.txt')
        es_valido, error = validar_archivo_python(archivo)
        assert not es_valido
        assert "debe tener extensión .py" in error

    def test_es_directorio(self, tmp_path):
        es_valido, error = validar_archivo_python(tmp_path)
        assert not es_valido
        assert "no es un archivo" in error

    def test_error_permisos(self, crear_archivo_temporal, monkeypatch):
        archivo = crear_archivo_temporal()
        
        def mock_open(*args, **kwargs):
            raise PermissionError("Sin permisos")
        monkeypatch.setattr(Path, "open", mock_open)
        
        es_valido, error = validar_archivo_python(archivo)
        assert not es_valido
        assert "Permiso denegado" in error

    def test_error_sistema(self, crear_archivo_temporal, monkeypatch):
        archivo = crear_archivo_temporal()
        
        def mock_exists(*args, **kwargs):
            raise OSError("Error del sistema")
        monkeypatch.setattr(Path, "exists", mock_exists)
        
        es_valido, error = validar_archivo_python(archivo)
        assert not es_valido
        assert "Error al acceder" in error

    def test_ruta_string(self, crear_archivo_temporal):
        archivo = crear_archivo_temporal()
        es_valido, error = validar_archivo_python(str(archivo))
        assert es_valido
        assert error == ""

    def test_ruta_path(self, crear_archivo_temporal):
        archivo = crear_archivo_temporal()
        es_valido, error = validar_archivo_python(Path(archivo))
        assert es_valido
        assert error == ""

    @pytest.mark.parametrize("nombre_archivo", [
        "archivo.py",
        "archivo_con_guiones.py",
        "archivo123.py",
        "ARCHIVO.PY",
        "archivo.Py"
    ])
    def test_nombres_archivo_validos(self, tmp_path, nombre_archivo):
        archivo = tmp_path / nombre_archivo
        archivo.write_text("")
        es_valido, error = validar_archivo_python(archivo)
        assert es_valido
        assert error == ""