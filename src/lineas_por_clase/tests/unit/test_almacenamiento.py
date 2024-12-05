# tests/unit/gestion_archivos/test_almacenamiento.py
import pytest
from pathlib import Path

from lineas_por_clase.core.gestion_archivos.almacenamiento_metricas import AlmacenamientoMetricas
from lineas_por_clase.models.metricas import MetricasArchivo, MetricasClase
from lineas_por_clase.tests.fixtures.json_metricas import METRICAS_REGISTRO_CLASES


class TestAlmacenamientoMetricas:
    @pytest.fixture
    def ruta_temporal(self, tmp_path):
        return tmp_path / "metricas_test.json"

    @pytest.fixture
    def almacenamiento(self, ruta_temporal):
        return AlmacenamientoMetricas(str(ruta_temporal))

    @pytest.fixture
    def metricas_clase_prueba(self):
        return MetricasClase(
            nombre_clase="TestClass",
            cantidad_metodos=3,
            lineas_fisicas=20
        )

    @pytest.fixture 
    def metricas_prueba(self, metricas_clase_prueba):
        return MetricasArchivo(
            nombre_archivo="test.py",
            clases=[metricas_clase_prueba]
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
        assert len(metricas_cargadas.clases) == 1
        assert metricas_cargadas.clases[0].nombre_clase == "TestClass"
        assert metricas_cargadas.clases[0].cantidad_metodos == 3
        assert metricas_cargadas.clases[0].lineas_fisicas == 20

    def test_actualizar_metricas(self, almacenamiento, metricas_prueba):
        # Primera guardada
        almacenamiento.guardar_metricas(metricas_prueba)
        
        # Actualización
        nueva_clase = MetricasClase("TestClass2", 4, 25)
        metricas_actualizadas = MetricasArchivo(
            nombre_archivo="test.py",
            clases=[nueva_clase]
        )
        almacenamiento.guardar_metricas(metricas_actualizadas)
        
        metricas_cargadas = almacenamiento.cargar_metricas("test.py")
        assert len(metricas_cargadas.clases) == 1
        assert metricas_cargadas.clases[0].nombre_clase == "TestClass2"
        assert metricas_cargadas.clases[0].cantidad_metodos == 4
        assert metricas_cargadas.clases[0].lineas_fisicas == 25

    def test_cargar_metricas_inexistentes(self, almacenamiento):
        metricas = almacenamiento.cargar_metricas("no_existe.py")
        assert metricas is None

    def test_obtener_todas_las_metricas(self, almacenamiento):
        # Guardar múltiples métricas
        clase1 = MetricasClase("TestClass1", 2, 15)
        clase2 = MetricasClase("TestClass2", 3, 20)
        
        metricas1 = MetricasArchivo("test1.py", [clase1])
        metricas2 = MetricasArchivo("test2.py", [clase2])
        
        almacenamiento.guardar_metricas(metricas1)
        almacenamiento.guardar_metricas(metricas2)
        
        todas_las_metricas = almacenamiento.obtener_todas_las_metricas()
        assert len(todas_las_metricas) == 2
        # tests/unit/gestion_archivos/test_almacenamiento.py (continuación)
        assert any(m.nombre_archivo == "test1.py" for m in todas_las_metricas)
        assert any(m.nombre_archivo == "test2.py" for m in todas_las_metricas)
        
        # Verificar contenido de métricas
        for metricas in todas_las_metricas:
            if metricas.nombre_archivo == "test1.py":
                assert len(metricas.clases) == 1
                assert metricas.clases[0].nombre_clase == "TestClass1"
                assert metricas.clases[0].cantidad_metodos == 2
                assert metricas.clases[0].lineas_fisicas == 15
            elif metricas.nombre_archivo == "test2.py":
                assert len(metricas.clases) == 1 
                assert metricas.clases[0].nombre_clase == "TestClass2"
                assert metricas.clases[0].cantidad_metodos == 3
                assert metricas.clases[0].lineas_fisicas == 20

    def test_multiples_clases_por_archivo(self, almacenamiento):
        clase1 = MetricasClase("TestClass1", 2, 15)
        clase2 = MetricasClase("TestClass2", 3, 20) 
        clase3 = MetricasClase("TestClass3", 1, 10)

        metricas = MetricasArchivo("test.py", [clase1, clase2, clase3])
        almacenamiento.guardar_metricas(metricas)

        metricas_cargadas = almacenamiento.cargar_metricas("test.py")
        assert len(metricas_cargadas.clases) == 3
        
        nombres_clases = [c.nombre_clase for c in metricas_cargadas.clases]
        assert "TestClass1" in nombres_clases
        assert "TestClass2" in nombres_clases 
        assert "TestClass3" in nombres_clases

    def test_multiples_archivos_registro(self, almacenamiento):
        for nombre_archivo, metricas_dict in METRICAS_REGISTRO_CLASES.items():
            metricas = MetricasArchivo(
                nombre_archivo=metricas_dict["nombre_archivo"],
                clases=[MetricasClase(**clase_dict) for clase_dict in metricas_dict["clases"]]
            )
            almacenamiento.guardar_metricas(metricas)
        
        todas_las_metricas = almacenamiento.obtener_todas_las_metricas()
        assert len(todas_las_metricas) == len(METRICAS_REGISTRO_CLASES)
        
        for metricas in todas_las_metricas:
            archivo_original = METRICAS_REGISTRO_CLASES[metricas.nombre_archivo]
            assert len(metricas.clases) == len(archivo_original["clases"])
            
            for clase_actual, clase_original in zip(metricas.clases, archivo_original["clases"]):
                assert clase_actual.nombre_clase == clase_original["nombre_clase"]
                assert clase_actual.cantidad_metodos == clase_original["cantidad_metodos"]
                assert clase_actual.lineas_fisicas == clase_original["lineas_fisicas"]