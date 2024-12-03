from analizador_cambios.core.contadores.analizador import AnalizadorCodigo
from analizador_cambios.core.arbol.comparador_principal import ComparadorVersiones
from analizador_cambios.core.arbol.generador_reporte import GeneradorReporte

analizador1 = AnalizadorCodigo()
resultado = analizador1.analizar_archivo("../data/ejemplo_v1.py","ejemplo_v1.py")
analizador2 = AnalizadorCodigo()
resultado = analizador2.analizar_archivo("../data/ejemplo_v2.py","ejemplo_v2.py")
comparador = ComparadorVersiones()
comparar = comparador.comparar_archivos(analizador1.arbol,analizador2.arbol)
print(GeneradorReporte().generar_reporte(comparar))
