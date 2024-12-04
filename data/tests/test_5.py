def factorial(n):
    """
    Calcula el factorial de un número usando un while en una sola línea.
    """
    result = 1;
    i = 1  # Inicialización
    while i <= n: result *= i; i += 1  # Cálculo del factorial en una sola línea
    return result

def main():
    try:
        num = int(input("Ingresa un número entero no negativo: "))
        if num < 0:
            print("El factorial no está definido para números negativos.")
        else:
            print(f"El factorial de {num} es: {factorial(num)}")
    except ValueError:
        print("Por favor, ingresa un número entero válido.")

if __name__ == "__main__":
    main()
