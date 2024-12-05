# tests/unit/gestion_archivos/test_almacenamiento.py
import pytest
from pathlib import Path

from contador_lineas.core.gestion_archivos.almacenamiento_metricas import AlmacenamientoMetricas
from contador_lineas.models.metricas import MetricasArchivo
from contador_lineas.tests.fixtures.json_metricas import METRICAS_REGISTRO

class TestAlmacenamientoMetricas:
    @pytest.fixture
    def ruta_temporal(self, tmp_path):
        return tmp_path / "metricas_test.json"

    @pytest.fixture
    def almacenamiento(self, ruta_temporal):
        return AlmacenamientoMetricas(str(ruta_temporal))

    @pytest.fixture
    def metricas_prueba(self):
        return MetricasArchivo(
            nombre_archivo="test.py",
            lineas_logicas=10,
            lineas_fisicas=20
        )

    def test_inicializacion_archivo(self, ruta_temporal):
        AlmacenamientoMetricas(str(ruta_temporal))
        assert ruta_temporal.exists()
        assert ruta_temporal.read_text() == "{}"

    def test_guardar_metricas(self, almacenamiento, metricas_prueba):
        almacenamiento.guardar_metricas(metricas_prueba)
        metricas_cargadas = almacenamiento.cargar_metricas("test.py")
        assert metricas_cargadas is not None
        assert metricas_cargadas.nombre_archivo == "test.py"
        assert metricas_cargadas.lineas_logicas == 10
        assert metricas_cargadas.lineas_fisicas == 20

    def test_actualizar_metricas(self, almacenamiento, metricas_prueba):
        # Primera guardada
        almacenamiento.guardar_metricas(metricas_prueba)
        
        # Actualización
        metricas_actualizadas = MetricasArchivo(
            nombre_archivo="test.py",
            lineas_logicas=15,
            lineas_fisicas=25
        )
        almacenamiento.guardar_metricas(metricas_actualizadas)
        
        metricas_cargadas = almacenamiento.cargar_metricas("test.py")
        assert metricas_cargadas.lineas_logicas == 15
        assert metricas_cargadas.lineas_fisicas == 25

    def test_cargar_metricas_inexistentes(self, almacenamiento):
        metricas = almacenamiento.cargar_metricas("no_existe.py")
        assert metricas is None

    def test_obtener_todas_las_metricas(self, almacenamiento):
        # Guardar múltiples métricas
        metricas1 = MetricasArchivo("test1.py", 10, 20)
        metricas2 = MetricasArchivo("test2.py", 15, 25)
        
        almacenamiento.guardar_metricas(metricas1)
        almacenamiento.guardar_metricas(metricas2)
        
        todas_las_metricas = almacenamiento.obtener_todas_las_metricas()
        assert len(todas_las_metricas) == 2
        assert any(m.nombre_archivo == "test1.py" for m in todas_las_metricas)
        assert any(m.nombre_archivo == "test2.py" for m in todas_las_metricas)

    def test_multiples_archivos_registro(self, almacenamiento):
        for nombre_archivo, metricas_dict in METRICAS_REGISTRO.items():
            metricas = MetricasArchivo(**metricas_dict)
            almacenamiento.guardar_metricas(metricas)
        
        todas_las_metricas = almacenamiento.obtener_todas_las_metricas()
        assert len(todas_las_metricas) == len(METRICAS_REGISTRO)
        for metricas in todas_las_metricas:
            assert metricas.nombre_archivo in METRICAS_REGISTRO
            original = METRICAS_REGISTRO[metricas.nombre_archivo]
            assert metricas.lineas_logicas == original['lineas_logicas']
            assert metricas.lineas_fisicas == original['lineas_fisicas']