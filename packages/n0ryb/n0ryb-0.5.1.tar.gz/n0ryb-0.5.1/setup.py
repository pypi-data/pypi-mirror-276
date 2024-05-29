from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Configuración del paquete
setup(
    name="n0ryb",
    version="0.5.1",
    packages=find_packages(),
    install_requires=[],  # Corrige la lista vacía
    author="NORYB Profesor: S4vitar",
    description="Una prueba para consultar biblioteca de la academia hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
