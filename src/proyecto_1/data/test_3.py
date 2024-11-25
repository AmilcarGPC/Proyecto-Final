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

def main():
    try:
        # Entrada del usuario
        num = float(input("Ingresa un número: "))
        # Clasificación del número
        category = categorize_number(num)
        print(f"El número {num} pertenece a la categoría: {category}")
    except ValueError:
        print("Por favor, ingresa un número válido.")

if __name__ == "__main__":
    main()
