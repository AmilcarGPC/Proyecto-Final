---
# docs/estimaciones/proyecto_1.md
title: Estimación del Sistema de Conteo de LOC
description: Estimación en Puntos de Función para el sistema de conteo de líneas de código
---

## 1. Información General

| Campo | Valor |
|-------|-------|
| Proyecto | Sistema de Conteo de LOC |
| Tipo de Estimación | Macroestimación (inicio del proyecto) |
| Fecha Estimación | 13-11-2024 |
| Estimador | Amílcar Pérez |
| Versión | 1.0 |
| Metodología | Puntos Funcionales |

## 2. Funciones de Datos

### 2.1 Archivos Lógicos 
#### Archivos Lógicos Internos (ILF)
| Nombre | Descripción | Complejidad | PF |
|--------|-------------|-------------|------|
| Base de datos de métricas | Almacena historial de LOC físicas y lógicas de archivos analizados | Simple | 7 |
| Configuración de conteo | Guarda reglas y parámetros para el análisis de código | Simple | 7 |

#### Archivos Lógicos Externos (EIF)
| Nombre | Descripción | Complejidad | PF |
|--------|-------------|-------------|------|
| Archivos fuente Python | Archivos .py que serán analizados para el conteo de líneas | Simple | 5 |

### 2.2 Funciones de Transaccioness
#### Entradas Externas (EI)
| Nombre | Descripción | Complejidad | PF |
|--------|-------------|-------------|------|
| Ingreso ruta archivo | Permite al usuario especificar la ubicación del archivo a analizar | Simple | 3 |
| Solicitud análisis | Indica al sistema iniciar con el proceso de conteo de líneas en el archivo seleccionado | Simple | 3 |

#### Salidas Externas (EO)
| Nombre | Descripción | Complejidad | PF |
|--------|-------------|-------------|------|
| Tabla resultados | Muestra el resumen de LOC físicas y lógicas por archivo | Simple | 4 |

#### Consultas Externas (EQ)
| Nombre | Descripción | Complejidad | PF |
|--------|-------------|-------------|------|
| Consulta métricas programa | Permite buscar las métricas de un programa específico | Simple | 3 |

## 3. Puntos de Función Sin Ajustar

| Elemento | Cantidad | Simple | Promedio | Complejo | Total |
|----------|----------|---------|-----------|-----------|--------|
| Entradas externas | 2 | 2 (peso: 3) | 0 | 0 | 6 |
| Salidas externas | 1 | 1 (peso: 4) | 0 | 0 | 4 |
| Consultas externas | 1 | 1 (peso: 3) | 0 | 0 | 3 |
| Archivos lógicos externos | 1 | 1 (peso: 7) | 0 | 0 | 7 |
| Archivos lógicos internos | 2 | 2 (peso: 5) | 0 | 0 | 10 |
| **Total** | | | | | **30** |

## 4. Factores de Complejidad Técnica

| Factor | Descripción | Valor | Justificación |
|--------|-------------|-------|---------------|
| F_1 | Fiabilidad backup/recovery | 2 | Backup básico de archivos |
| F_2 | Funciones distribuidas | 0 | Sistema único |
| F_3 | Configuración | 1 | Config básica |
| F_4 | Facilidad operativa | 3 | Interface amigable |
| F_5 | Complejidad interfaz | 2 | I/O simple |
| F_6 | Reutilización | 4 | Alta reusabilidad |
| F_7 | Instalaciones múltiples | 0 | Única instalación |
| F_8 | Comunicaciones | 0 | Sin red |
| F_9 | Desempeño | 2 | Básico |
| F_10 | Entrada datos online | 1 | Input básico |
| F_11 | Actualización online | 1 | Updates simples |
| F_12 | Procesamiento complejo | 3 | Análisis de código |
| F_13 | Facilidad instalación | 1 | Simple |
| F_14 | Facilidad cambio | 3 | Mantenible |
| **Total** | | **23** | |

## 5. Cálculo Final

### 5.1 Factor de Ajuste Técnico (TCF)
TCF = 0.65 + 0.01 * Σ(F_i) TCF = 0.65 + 0.01 * 23 TCF = 0.88

### 5.2 Puntos de Función
| Tipo | Valor |
|------|--------|
| Puntos sin ajustar (UFP) | 30 |
| Factor de ajuste (TCF) | 0.88 |
| **Puntos ajustados (AFP)** | 30*0.88 = **26.4** |

## 6. Estimación de Esfuerzo

### 6.1 Parámetros
| Parámetro | Valor |
|-----------|--------|
| Horas por PF | 8 |
| Horas laborales/día | 8 |
| Días laborales/semana | 5 |

### 6.2 Cálculo de Tiempo
```
Horas totales = AFP * Horas por PF = 26.4 * 8 = 211.2 horas
Días laborales = 211.2 / 8 = 26.4 días
Semanas = 26.4 / 5 ≈ 6 semanas
```

## 7. Resumen Final

| Métrica | Valor |
|---------|--------|
| Puntos de Función Ajustados | 26.4 |
| Horas estimadas | 211.2 |
| Días laborales | 26.4 |
| Semanas estimadas para un desarrollador | 6 semanas |
| Semanas estimadas para 5 desarrolladores | 6 días |
| Fecha estimada fin | 19-11-2024 |