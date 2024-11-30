from setuptools import setup, find_packages

setup(
    name="sistema_conteo_lineas_y_analisis_cambios",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "colorama",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "contador_lineas=contador_lineas.__main__:main",
            "lineas_por_clase=lineas_por_clase.__main__:main",
            "analizador_cambios=analizador_cambios.__main__:main",
        ],
    }
)