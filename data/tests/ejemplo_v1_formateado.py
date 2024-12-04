# Caso 1: Comentario en línea de continuación
valor1 = 1
valor2 = 2
valor3 = 3
valor4 = 4

elemento1 = 1
elemento2 = 2

result = (valor1 + valor2 + valor3 + valor4 + 
          valor2)

# Caso 2: Comentario en parámetro de función
def funcion(
    param1,  # Este comentario podría causar error de sintaxis
    param2):
    return 0

# Entrada
mi_lista = [
    elemento1, elemento2, elemento1, elemento2, elemento1,
    # Este comentario romperá la continuación porque es muy largo, entonces
    # deberá dividirse en varias líneas
    elemento1, elemento2, elemento1, elemento2, elemento1
    # Descripción del elemento 2
]

# Entrada
mi_funcion(
    argumento1="valor", argumento2=123,argumento3=3, argumento4=4, \
    argumento5=5, argumento6=6
    # Explica el primer argumento
)

