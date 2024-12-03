# Caso 1: Comentario en línea de continuación
result = (valor1 + valor2 + valor3 + valor4 # Este comentario romperá la continuación
          valor2)

# Caso 2: Comentario en parámetro de función
def funcion(
    param1,  # Este comentario podría causar error de sintaxis
    param2):
    return 0