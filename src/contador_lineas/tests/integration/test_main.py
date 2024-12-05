# tests/integration/test_main.py
import pytest
from pathlib import Path

from contador_lineas.__main__ import (
    obtener_nombre_archivo,
    procesar_argumentos,
    validar_argumentos,
    procesar_archivo,
    main
)
from contador_lineas.core.gestion_archivos.almacenamiento_metricas import AlmacenamientoMetricas
from contador_lineas.tests.fixtures.estructuras_basicas import *

class TestMainIntegracion:
    @pytest.fixture
    def crear_archivo_temporal(self, tmp_path):
        def _crear_archivo(contenido: str, nombre="test.py") -> Path:
            archivo = tmp_path / nombre
            archivo.write_text(contenido)
            return archivo
        return _crear_archivo

    @pytest.fixture
    def mock_args(self, monkeypatch):
        def _mock_args(args_list):
            monkeypatch.setattr("sys.argv", ["contador_lineas"] + args_list)
        return _mock_args

    def test_obtener_nombre_archivo(self):
        casos = [
            ("archivo.py", "archivo.py"),
            ("ruta/archivo.py", "archivo.py"),
            ("C:/ruta/archivo.py", "archivo.py"),
            ("./archivo.py", "archivo.py")
        ]
        for entrada, esperado in casos:
            assert obtener_nombre_archivo(entrada) == esperado

    def test_procesar_argumentos_archivo_simple(self, mock_args):
        mock_args(["archivo.py", '--dev-db-path', "tests.json"])
        args = procesar_argumentos()
        assert args.ruta_archivo == "archivo.py"
        assert not args.t
        assert not args.tc

    def test_procesar_argumentos_tabla_individual(self, mock_args):
        mock_args(["archivo.py", "-t", '--dev-db-path', "tests.json"])
        args = procesar_argumentos()
        assert args.ruta_archivo == "archivo.py"
        assert args.t
        assert not args.tc

    def test_procesar_argumentos_tabla_completa(self, mock_args):
        mock_args(["-tc", '--dev-db-path', '"tests.json"'])
        args = procesar_argumentos()
        assert args.ruta_archivo is None
        assert not args.t
        assert args.tc

    def test_validar_argumentos_validos(self):
        casos = [
            (("archivo.py", False, False), True),
            (("archivo.py", True, False), True),
            ((None, False, True), True),
            (("archivo.py", True, True), True)
        ]
        for (archivo, t, tc), esperado in casos:
            args = type('Args', (), {'ruta_archivo': archivo, 't': t, 'tc': tc})()
            es_valido, _ = validar_argumentos(args)
            assert es_valido == esperado

    def test_validar_argumentos_invalidos(self):
        args = type('Args', (), {'ruta_archivo': None, 't': False, 'tc': False})()
        es_valido, mensaje = validar_argumentos(args)
        assert not es_valido
        assert "Se requiere el archivo" in mensaje

    def test_procesar_archivo_exitoso(self, crear_archivo_temporal, tmp_path):
        archivo = crear_archivo_temporal(FUNCION_BASICA)
        almacen = AlmacenamientoMetricas("tests.json")
        
        procesar_archivo(str(archivo), "tests.json", almacen, True)
        
        metricas = almacen.cargar_metricas("test.py")
        assert metricas is not None
        assert metricas.lineas_fisicas == 2
        assert metricas.lineas_logicas == 1

    def test_main_archivo_simple(self, crear_archivo_temporal, mock_args, capsys):
        archivo = crear_archivo_temporal(FUNCION_BASICA)
        mock_args([str(archivo), '--dev-db-path', "tests.json"])
        main()
        
        captured = capsys.readouterr()
        assert "¡Archivo procesado exitosamente!" in captured.out

    def test_main_archivo_con_tabla(self, crear_archivo_temporal, mock_args, capsys):
        archivo = crear_archivo_temporal(FUNCION_BASICA)
        mock_args([str(archivo), "-t", '--dev-db-path', "tests.json"])
        main()
        
        captured = capsys.readouterr()
        assert "¡Archivo procesado exitosamente!" in captured.out
        assert "LOC Físicas" in captured.out
        assert "LOC Lógicas" in captured.out
        assert "test.py" in captured.out

    def test_main_tabla_completa(self, crear_archivo_temporal, mock_args, capsys):
        # Crear varios archivos para tener métricas históricas
        archivos = [
            ("test1.py", FUNCION_BASICA),
            ("test2.py", CLASE_BASICA),
            ("test3.py", FUNCION_CON_PARAMETROS)
        ]
        for nombre, contenido in archivos:
            archivo = crear_archivo_temporal(contenido, nombre)
            mock_args([str(archivo), '--dev-db-path', "tests.json"])
            main()
        
        # Solicitar tabla completa
        mock_args(["-tc", '--dev-db-path', "tests.json"])
        main()
        
        captured = capsys.readouterr()
        assert "PROGRAMA" in captured.out
        for nombre, _ in archivos:
            assert nombre in captured.out

    def test_main_error_archivo_invalido(self, mock_args, capsys):
        mock_args(["no_existe.py", '--dev-db-path', "tests.json"])
        main()
        
        captured = capsys.readouterr()
        assert "Archivo inválido" in captured.out

    def test_main_error_archivo_viola_estandar(self, crear_archivo_temporal, mock_args, capsys):
        contenido = "x = 1; y = 2\n"  # Múltiples declaraciones
        archivo = crear_archivo_temporal(contenido)
        mock_args([str(archivo), '--dev-db-path', "tests.json"])
        main()
        
        captured = capsys.readouterr()
        assert "Violación del estándar" in captured.out

    def test_main_sin_argumentos(self, mock_args, capsys):
        mock_args(['--dev-db-path', "tests.json"])
        main()
        
        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "Se requiere el archivo cuando no se usa -tc" in captured.out