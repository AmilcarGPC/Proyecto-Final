def generate_even_squares(limit):
    """
    Genera una lista de pares y sus cuadrados hasta un límite.
    """
    numbers = [n for n in range(limit + 1) if n % 2 == 0]  # Números pares
    squares = [n ** 2 for n in numbers]; print(f"Números: {numbers}")  # Uso de ';'
    return squares

def main():
    try:
        limit = int(input("Ingresa el límite superior: "))
        squares = generate_even_squares(limit)
        print(f"Cuadrados: {squares}")
    except ValueError:
        print("Por favor, ingresa un número entero válido.")

if __name__ == "__main__":
    main()
