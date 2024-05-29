import setuptools
from pathlib import Path

# Ruta del redme para colocarlo como descripción.
long_desc = Path("README.md").read_text()

setuptools.setup(
    name="holamundoplayer20",
    version="0.0.1",
    long_description=long_desc,
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    )
)
