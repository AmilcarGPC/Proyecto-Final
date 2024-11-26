from setuptools import setup, find_packages

setup(
    name="contador_lineas",
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
        ],
    }
)