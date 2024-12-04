---
# docs/estandares/estandar_codificacion/4_importaciones.md
title: Importaciones
description: Esta sección describe las reglas y mejores prácticas para importar módulos y librerías en Python. Incluye ejemplos y recomendaciones.
---

Este documento establece las convenciones para organizar y estructurar las importaciones en código Python, siguiendo las recomendaciones y las mejores prácticas. El objetivo es mantener el código ordenado, eficiente y fácil de mantener.


## 1. Orden de Imports

### Instrucciones
- Seguir orden: módulos estándar, third-party, locales
- Separar grupos con una línea en blanco
- Ordenar alfabéticamente dentro de cada grupo
- Imports absolutos antes que relativos

### Mejores Prácticas
- Evitar imports circulares
- No usar import *
- Mantener imports al inicio del archivo
- Limitar el uso a módulos específicos

### Ejemplos
```python
# Correct
import os
import sys

import numpy as np
import pandas as pd

from app.core import settings
from app.utils import helpers

# Wrong
from app.utils import helpers
import os
from app.core import *
```

### Verificación
- [ ] ¿Grupos separados correctamente?
- [ ] ¿Orden alfabético en cada grupo?
- [ ] ¿Módulos concretos en lugar de *?
- [ ] ¿Sin imports circulares o wildcards?

## 2. Agrupación de Imports

### Instrucciones
- Agrupar por tipo de import (import vs. from)
- Mantener imports relacionados juntos
- Usar alias consistentes y estándar
- Evitar imports redundantes

### Mejores Prácticas
- Evitar imports anidados
- Preferir imports explícitos
- Mantener consistencia en todo el proyecto
- Documentar alias no estándar

### Ejemplos
```python
# Correct
import numpy as np
import pandas as pd
import (scipy, sklearn, tensorflow)
from matplotlib import pyplot as plt

from aplicacion.models import (
    Usuario,
    Perfil,
    Configuracion
)

# Wrong
import numpy
from numpy import array as arr
from numpy.random import *
```

### Verificación
- [ ] ¿Agrupación lógica?
- [ ] ¿Alias estándar?
- [ ] ¿Imports explícitos?
- [ ] ¿Sin imports anidados excesivos?

## 3. Imports Absolutos vs Relativos

### Instrucciones
- Preferir imports absolutos
- Evitar imports relativos (..)
- Usar imports relativos solo en paquetes
- Mantener estructura clara de módulos
- Evitar dependencias circulares

### Mejores Prácticas
- Estructurar proyecto claramente
- Usar imports absolutos desde raíz
- Minimizar profundidad de imports
- Documentar estructura de imports
- Evitar imports dinámicos

### Ejemplos
```python
# Correct
from miproyecto.utils.helpers import formatear_fecha
from miproyecto.core.models import Usuario

# Wrong
from ...utils.helpers import formatear_fecha
from .models import *
```

### Verificación
- [ ] ¿Principalmente imports absolutos?
- [ ] ¿Estructura clara de módulos?
- [ ] ¿Sin imports circulares?
- [ ] ¿Imports desde raíz del proyecto?

## 4. Alias Estándar

### Instrucciones
- Usar alias convencionales para librerías comunes
- Documentar alias no estándar
- Mantener consistencia en todo el proyecto
- Evitar nombres confusos o ambiguos
- Limitar uso de alias a casos necesarios

### Mejores Prácticas
- numpy -> np
- pandas -> pd
- matplotlib.pyplot -> plt
- tensorflow -> tf
- scipy -> sp

### Ejemplos
```python
# Correct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

# Wrong
import numpy as lib_numpy
import pandas as datos
import matplotlib.pyplot as grafico
```

### Verificación
- [ ] ¿Alias estándar para librerías comunes?
- [ ] ¿Consistencia en todo el proyecto?
- [ ] ¿Documentación para alias no estándar?
- [ ] ¿Nombres claros y no ambiguos?