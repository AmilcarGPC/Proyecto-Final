from cx_Freeze import setup, Executable
from setuptools import find_packages
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "colorama",
        "tabulate",
        "pathlib",
        "argparse",
        "typing",
        "json"
    ],
    "excludes": [],
    "include_files": [
        # Include your JSON database files
        ("db/metricas_registro.json", "db/metricas_registro.json"),
        ("db/lineas_por_clase_registro.json", "db/lineas_por_clase_registro.json")
    ]
}

# Base for the executable
base = None
if sys.platform == "win32":
    base = "Console"

executables = [
    Executable(
        "src/contador_lineas/__main__.py",
        base=base,
        target_name="contador_lineas.exe"
    ),
    Executable(
        "src/lineas_por_clase/__main__.py",
        base=base,
        target_name="lineas_por_clase.exe"
    ),
    Executable(
        "src/analizador_cambios/__main__.py",
        base=base,
        target_name="analizador_cambios.exe"
    )
]

setup(
    name="sistema_conteo_lineas_y_analisis_cambios",
    version="0.1.0",
    description="Sistema de análisis de código Python",
    options={
        "build_exe": build_exe_options
    },
    executables=executables,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "colorama",
        "tabulate",
    ],
)