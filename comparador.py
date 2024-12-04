import os
import subprocess

def recorrer_y_comparar(dir_a, dir_b):
    # Crear listas de archivos con sus rutas relativas
    archivos_a = {}
    archivos_b = {}

    # Recorrer recursivamente el directorio A
    for root, _, files in os.walk(dir_a):
        for file in files:
            if file.endswith(".py") and not file.endswith("_comentado.py"):
                rel_path = os.path.relpath(os.path.join(root, file), dir_a)
                archivos_a[rel_path] = os.path.join(root, file)

    # Recorrer recursivamente el directorio B
    for root, _, files in os.walk(dir_b):
        for file in files:
            if file.endswith(".py") and not file.endswith("_comentado.py"):
                rel_path = os.path.relpath(os.path.join(root, file), dir_b)
                archivos_b[rel_path] = os.path.join(root, file)

    # Comparar y ejecutar analizador_cambios
    for rel_path in archivos_a.keys():
        if rel_path in archivos_b:  # Si el archivo existe en ambos
            path_a = archivos_a[rel_path]
            path_b = archivos_b[rel_path]
            print(f"Analizando cambios entre: {path_a} y {path_b}")
            subprocess.run(["analizador_cambios", path_a, path_b, "-cc"])
        else:
            print(f"Archivo presente solo en directorio A: {archivos_a[rel_path]}")

    # Verificar archivos que están en B pero no en A
    for rel_path in archivos_b.keys():
        if rel_path not in archivos_a:
            print(f"Archivo presente solo en directorio B: {archivos_b[rel_path]}")

# Directorios a comparar
dir_a = "data/a"  # Cambia esto por el path real
dir_b = "data/b"  # Cambia esto por el path real

recorrer_y_comparar(dir_a, dir_b)