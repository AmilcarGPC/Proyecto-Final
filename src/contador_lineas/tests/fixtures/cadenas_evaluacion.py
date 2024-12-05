CASOS_CADENAS_CERRADAS = [
    {
        'codigo': '"texto completo"',
        'posicion': 5,
        'esperado_simple': True,
        'esperado_cerrado': True,
        'descripcion': 'Cadena completa'
    },
    {
        'codigo': '"texto sin cerrar',
        'posicion': 5,
        'esperado_simple': True,
        'esperado_cerrado': False,
        'descripcion': 'Cadena sin cerrar'
    },
    {
        'codigo': '''texto "en medio" más''',
        'posicion': 8,
        'esperado_simple': True,
        'esperado_cerrado': True,
        'descripcion': 'Cadena en medio'
    },
    {
        'codigo': '''var = "'mezclado'"''',
        'posicion': 8,
        'esperado_simple': True,
        'esperado_cerrado': True,
        'descripcion': 'Comillas mezcladas'
    },
    {
        'codigo': '''f"texto {variable} texto"''',
        'posicion': 10,
        'esperado_simple': True,
        'esperado_cerrado': True,
        'descripcion': 'f-string'
    },
    {
        'codigo': '"texto\\"escapado"',
        'posicion': 7,
        'esperado_simple': True,
        'esperado_cerrado': True,
        'descripcion': 'Escape'
    },
    {
        'codigo': """'''texto\nmultilinea'''""",
        'posicion': 12,
        'esperado_simple': True,
        'esperado_cerrado': True,
        'descripcion': 'Multilinea'
    }
]

CASOS_ENCONTRAR = [
    {
        'codigo': 'x = "texto = más"',
        'buscar': '=',
        'inicio': 0,
        'cerrado': True,
        'esperado_simple': 2,
        'esperado_cerrado': 2,
        'descripcion': 'Cadena simple'
    },
    {
        'codigo': 'if x == "y == z":',
        'buscar': '==',
        'inicio': 0,
        'cerrado': True,
        'esperado_simple': 5,
        'esperado_cerrado': 5,
        'descripcion': 'Operador =='
    },
    {
        'codigo': '''var = "sin cerrar''',
        'buscar': '=',
        'inicio': 0,
        'cerrado': True,
        'esperado_simple': 4,
        'esperado_cerrado': 4,
        'descripcion': 'Sin cerrar'
    },
    {
        'codigo': '''var = "texto" + "más"''',
        'buscar': '+',
        'inicio': 0,
        'cerrado': True,
        'esperado_simple': 14,
        'esperado_cerrado': -1,
        'descripcion': 'Concatenación'
    }
]

CASOS_CONTAR = [
    {
        'codigo': 'x = y = z = "a = b = c"',
        'caracter': '=',
        'esperado': 3,
        'descripcion': 'Múltiples asignaciones'
    },
    {
        'codigo': '''print("=") # = comentario''',
        'caracter': '=',
        'esperado': 0,
        'descripcion': 'Solo en cadena y comentario'
    },
    {
        'codigo': '''"""triple = quoted""" + '= simple' + "= doble"''',
        'caracter': '+',
        'esperado': 2,
        'descripcion': 'Concatenación múltiple'
    },
    {
        'codigo': r'''x = "escaped \"quote\" here = test"''',
        'caracter': '=',
        'esperado': 1,
        'descripcion': 'Comillas escapadas'
    }
]