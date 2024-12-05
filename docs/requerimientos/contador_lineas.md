# Descripción de Módulos

```Markdown
contador_lineas/
├── config/
│   └── node_types/
├── core/
│   ├── analizadores/
│   │   ├── analizador_cadenas.py
│   │   ├── analizador_comprehension.py
│   │   ├── analizador_corchetes.py
│   │   ├── analizador_expresiones.py
│   │   ├── analizador_ternario.py
│   │   └── buscar_y_extraaer_anidados.py
│   ├── árbol/
│   │   ├── analizador_nodos.py
│   │   ├── arbol_sintactico.py
│   │   ├── constructor_arbol.py
│   │   ├── nodo.py
│   │   └── verificador_estandar_codigo.py
│   ├── contadores/
│   │   ├── analizador.py
│   │   ├── contador_fisico.py
│   │   └── contador_logico.py
│   ├── gestion_archivos/
│   │   ├── almacenamiento_metricas.py
│   │   └── lector_archivo.py
│   └── constantes.py
├── models/
│   ├── métricas.py
│   └── nodos.py
├── tests/
├── utils/
│   ├── archivo_utils.py
│   ├── formateador_metricas.py
│   ├── impresion_arbol.py
│   └── validador.py
└── __main__.py
```

## Configuración
- **`contador_lineas/config/node_types.py`**  
  Define los conjuntos de tipos de nodos permitidos para el análisis de código Python.

## Núcleo

### Analizadores
- **`contador_lineas/core/analizadores/analizador_cadenas.py`**  
  Analiza y procesa cadenas de texto en código Python.
- **`contador_lineas/core/analizadores/analizador_comprehension.py`**  
  Analiza y procesa expresiones de comprehensions en código Python.
- **`contador_lineas/core/analizadores/analizador_corchetes.py`**  
  Analiza y encuentra pares de corchetes y límites de expresiones en código Python.
- **`contador_lineas/core/analizadores/analizador_expresiones.py`**  
  Analiza expresiones ternarias y comprehensions en código Python.
- **`contador_lineas/core/analizadores/analizador_ternario.py`**  
  Analiza y procesa expresiones ternarias en código Python.
- **`contador_lineas/core/analizadores/buscar_y_extraer_anidados.py`**  
  Analiza y extrae expresiones anidadas en código Python.

### Árbol
- **`contador_lineas/core/arbol/analizador_nodos.py`**  
  Analiza y clasifica tipos de nodos en código Python.
- **`contador_lineas/core/arbol/arbol_sintactico.py`**  
  Define la estructura del árbol sintáctico para archivos Python.
- **`contador_lineas/core/arbol/constructor_arbol.py`**  
  Construye un árbol sintáctico a partir de código Python.
- **`contador_lineas/core/arbol/nodo.py`**  
  Define la estructura base de nodos para el árbol sintáctico.
- **`contador_lineas/core/arbol/verificador_estandar_codigo.py`**  
  Verifica el cumplimiento de estándares de código Python en árboles sintácticos.

### Contadores
- **`contador_lineas/core/contadores/analizador.py`**  
  Analiza archivos Python para obtener métricas de líneas de código.
- **`contador_lineas/core/contadores/contador_fisico.py`**  
  Cuenta líneas físicas de código Python excluyendo comentarios.
- **`contador_lineas/core/contadores/contador_logico.py`**  
  Cuenta líneas lógicas de código Python.

### Constantes
- **`contador_lineas/core/constantes.py`**  
  Define constantes utilizadas en el análisis de código Python.

## Modelos
- **`contador_lineas/models/metricas.py`**  
  Define la estructura de datos para almacenar métricas (Líneas Físicas y Lógicas) de archivos Python.
- **`contador_lineas/models/nodos.py`**  
  Define los tipos de nodos y su estructura para el análisis sintáctico.

## Utilidades
- **`contador_lineas/utils/archivo_utils.py`**  
  Utilidades para operaciones con archivos.
- **`contador_lineas/utils/formateador_metricas.py`**  
  Procesa y formatea métricas de código para su visualización en tabla.
- **`contador_lineas/utils/impresion_arbol.py`**  
  Imprime la estructura de árbol de un archivo Python representado como árbol sintáctico.
- **`contador_lineas/utils/validador.py`**  
  Valida archivos Python y verifica su accesibilidad.

## Principal
- **`contador_lineas/__main__.py`**  
  Punto de entrada principal para el analizador de código Python.
