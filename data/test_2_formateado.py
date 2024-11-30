from collections import (
    Counter
)
import string, import itertools

def process_text(file_path):

    """

    Procesa un archivo de texto para contar palabras frecuentes.

    """

    try:

        with open(file_path, 'r') as f:

            # Lee el archivo, elimina puntuación y lo convierte a minúsculas

            text = f.read()

            words = [

                word.strip(string.punctuation).lower()

                for word in text.split()

                if len(word.strip(string.punctuation)) > 0

            ]

    except FileNotFoundError:

        return f"El archivo {file_path} no existe."

    

    # Contar palabras con Counter

    counter = Counter(words)

    top_words = counter.most_common(5)


    # Usamos un generator expression para formatear la salida

    return '\n'.join(

        f"{word}: {count}" for word, count in top_words

    ) if top_words else "No se encontraron palabras."


def main():

    # Archivo de ejemplo

    file_path = "texto_ejemplo.txt"


    # Operador ternario para imprimir resultado o error

    result = process_text(file_path)

    print(result if isinstance(result, str) else "Procesamiento fallido.")


if __name__ == "__main__":

    main()

