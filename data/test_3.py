def categorize_number(num):
    """
    Clasifica un número en una categoría específica.
    """
    return (
        "Negativo" if num < 0 
        else "Cero" if num == 0 
        else "Pequeño positivo" if num <= 10 
        else "Mediano" if num <= 100 
        else "Grande"
    )