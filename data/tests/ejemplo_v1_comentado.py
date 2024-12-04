# Caso 1: Comentario en línea de continuación # ELIMINADA
valor1 = 1 # ELIMINADA
valor2 = 2 # ELIMINADA
valor3 = 3 # ELIMINADA
valor4 = 4 # ELIMINADA

elemento1 = 1 # ELIMINADA
elemento2 = 2 # ELIMINADA

result = (valor1 + valor2 + valor3 + valor4 + 
          valor2) # ELIMINADA (las 2 líneas previas cuentan como 1)

# Caso 2: Comentario en parámetro de función # ELIMINADA
def funcion(
    param1,  # Este comentario podría causar error de sintaxis
    param2): # ELIMINADA (las 3 líneas previas cuentan como 1)
    return 0 # ELIMINADA

# Entrada # ELIMINADA
mi_lista = [
    elemento1, elemento2, elemento1, elemento2, elemento1,
    # Este comentario romperá la continuación porque es muy largo, entonces deberá dividirse en varias líneas
    elemento1, elemento2, elemento1, elemento2, elemento1
    # Descripción del elemento 2
] # ELIMINADA (las 6 líneas previas cuentan como 1)

# Entrada # ELIMINADA
mi_funcion(
    argumento1="valor", argumento2=123,argumento3=3, argumento4=4, argumento5=5, argumento6=6
    # Explica el primer argumento
) # ELIMINADA (las 4 líneas previas cuentan como 1)

