---
# docs/estandares/aseguramiento_calidad.md
title: Aseguramiento de la Calidad
description: Este documento incluye las prácticas y procesos para asegurar la calidad del software. Se describen las fases de desarrollo, procesos de control de calidad, roles y responsabilidades, herramientas y recursos, y métricas de calidad.
---

## 1. Fases de Desarrollo

### 1.1 Planeación del Proyecto
- **Project Manager**:
  - Divide las tareas usando GitHub Projects
  - Establece prioridades y fechas límite
  - Define los entregables principales
- **Equipo Completo**: 
  - Participa en reuniones de planificación semanales
  - Estima tiempo de tareas
  - Identifica riesgos potenciales

### 1.2 Diseño del Sistema
- **Líder Técnico**:
  - Crea diagramas de arquitectura
  - Define componentes principales
  - Establece patrones de diseño a utilizar
- **Equipo de Desarrollo**:
  - Participa en sesiones de diseño
  - Revisa y propone mejoras al diseño
  - Documenta decisiones técnicas en Wiki

### 1.3 Desarrollo de Software
- **Desarrolladores**:
  - Siguen estándar de codificación establecido
  - Utilizan GitHub Actions para verificación automática
  - Aplican herramientas como pylint/eslint
- **Revisores**:
  - Realizan code reviews usando pull requests
  - Verifican cumplimiento de estándares
  - Sugieren mejoras de código

### 1.4 Aseguramiento de Calidad
- **Equipo QA**:
  - Ejecuta pruebas unitarias (cobertura >70%)
  - Realiza pruebas de integración
  - Verifica requisitos funcionales
  - Documenta casos de prueba

## 2. Procesos de Control de Calidad

### 2.1 Inspección Pre-Cliente (Semanal)
```
- Asignación de roles
- Revisión de código completado
- Verificación de documentación
- Lista de pendientes/problemas
```

### 2.2 Punto de Control Sábado
```
- Reporte individual de avances
- Discusión de problemas
- Revisión de métricas de calidad
- Planeación siguiente semana
```

## 3. Roles y Responsabilidades

### 3.1 Equipo de Desarrollo
- **Líder Técnico**:
  - Guía técnica del proyecto
  - Revisión final de código
  - Aprobación de cambios mayores
- **Desarrolladores**:
  - Implementación de funcionalidades
  - Documentación de código
  - Pruebas unitarias

### 3.2 Equipo de Calidad
- **Responsable QA**:
  - Verifica cumplimiento de procesos
  - Verifica que se cumpla el estándar de codificación
  - Ejecuta pruebas de sistema
  - Mantiene métricas de calidad
- **Analista QA**:
  - Diseña casos de prueba
  - Reporta y verifica bugs
  - Pruebas de regresión

### 3.3 Documentación
- **Documentador**:
  - Mantiene manuales actualizados
  - Documenta decisiones técnicas

## 4. Herramientas y Recursos

### 4.1 Control de Versiones
```
- Git/GitHub para código
- Ramas feature/ para desarrollo
- Pull requests obligatorios
- Commits significativos y bien documentados
```

### 4.2 Calidad de Código
```
- GitHub Actions para CI/CD
- Pylint para estándares
```

### 4.3 Seguimiento
```
- GitHub Projects para tareas
- GitHub Issues para bugs
- Documentación
- Discord para comunicación
```

## 5. Métricas de Calidad

### 5.1 Indicadores Clave
```
- Número de bugs encontrados por modulo
```