# Plan de Pruebas - Contador de Líneas

```Markdown
contador_lineas/
└── tests/
    ├── unit/              # Pruebas unitarias
    │   ├── contadores/    # Tests for counters
    │   ├── analizadores/  # Tests for analyzers
    │   ├── arbol/        # Tests for tree components
    │   └── utils/         # Tests for utilities
    ├── integration/       # Pruebas de integración
    ├── fixtures/         # Test data files
    └── conftest.py       # PyTest shared fixtures# Plan de Pruebas - Contador de Líneas
```

## Pruebas Unitarias

### 1. Módulos Core/Contadores
- `test_contador_fisico.py`:
    - Contar líneas en archivo vacío
    - Contar líneas con comentarios
    - Contar líneas en blanco
    - Contar líneas con código mezclado
    
- `test_contador_logico.py`:
    - Verificar expresiones multilínea
    - Verificar comprehensions
    - Verificar expresiones ternarias
    - Verificar decoradores

### 2. Módulos de Análisis
- `test_analizador_cadenas.py`:
    - Strings multilínea
    - f-strings
    - Strings con escape characters
    
- `test_analizador_expresiones.py`:
    - List comprehensions
    - Dictionary comprehensions
    - Expresiones ternarias anidadas

### 3. Módulos de Árbol
- `test_constructor_arbol.py`:
    - Construcción básica de árbol
    - Manejo de imports
    - Manejo de clases y métodos
    - Manejo de funciones anidadas

### 4. Módulos de Utilidades
- `test_validador.py`:
    - Validación de archivos Python válidos
    - Manejo de archivos no existentes
    - Manejo de permisos incorrectos

## Pruebas de Integración

### 1. Flujo Completo
- `test_integracion_analisis.py`:
    ```python
    def test_flujo_analisis_completo():
            # Preparar archivo de prueba
            contenido = """
            def ejemplo():
                    # Comentario
                    return [x for x in range(10) 
                                 if x % 2 == 0]
            """
            # Verificar métricas físicas y lógicas
            assert metricas.lineas_fisicas == 5
            assert metricas.lineas_logicas == 2
    ```

### 2. Almacenamiento de Métricas
- `test_integracion_metricas.py`:
    ```python
    def test_almacenamiento_metricas():
            # Analizar archivo
            # Verificar almacenamiento correcto
            # Verificar recuperación de métricas
    ```

## Escenarios de Prueba End-to-End

1. Análisis de Proyecto Completo:
     ```python
     def test_analisis_proyecto():
             # Preparar estructura de proyecto
             # Ejecutar análisis
             # Verificar resultados agregados
     ```

2. Generación de Reportes:
     ```python
     def test_generacion_reportes():
             # Analizar múltiples archivos
             # Generar reporte
             # Verificar formato y contenido
     ```

## Casos Edge y Error

1. Manejo de Errores:
     - Archivos malformados
     - Sintaxis Python inválida
     - Rutas no existentes
     - Permisos insuficientes

2. Casos Especiales:
     - Archivos muy grandes
     - Nombres de archivo no estándar
     - Caracteres especiales en rutas

## Fixture Files
