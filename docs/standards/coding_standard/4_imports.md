---
# docs/standards/coding_standard/imports.md
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
- Un import por línea

### Mejores Prácticas
- Evitar imports circulares
- No usar import *
- Mantener imports al inicio del archivo
- Limitar el uso a módulos específicos
- Evitar imports dinámicos

### Ejemplos
```python
# Correct
import os
import sys

import numpy as np
import pandas as pd

from myapp.core import settings
from myapp.utils import helpers

# Wrong
from myapp.utils import *
import sys, os
import pandas as pd, numpy as np
```

### Verificación
- [ ] ¿Grupos separados correctamente?
- [ ] ¿Orden alfabético en cada grupo?
- [ ] ¿Un import por línea?
- [ ] ¿Sin imports circulares o wildcards?

## 2. Agrupación de Imports

### Instrucciones
- Agrupar por tipo de import (import vs. from)
- Mantener imports relacionados juntos
- Usar alias consistentes y estándar
- Evitar imports redundantes
- Máximo 3 niveles de profundidad en imports

### Mejores Prácticas
- Usar alias estándar (np, pd, plt)
- Evitar imports anidados
- Preferir imports explícitos
- Mantener consistencia en todo el proyecto
- Documentar alias no estándar

### Ejemplos
```python
# Correct
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from myapp.models import (
    User,
    Profile,
    Settings
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
from myproject.utils.helpers import format_date
from myproject.core.models import User

# Wrong
from ...utils.helpers import format_date
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
import numpy as numpy_lib
import pandas as data
import matplotlib.pyplot as graph
```

### Verificación
- [ ] ¿Alias estándar para librerías comunes?
- [ ] ¿Consistencia en todo el proyecto?
- [ ] ¿Documentación para alias no estándar?
- [ ] ¿Nombres claros y no ambiguos?