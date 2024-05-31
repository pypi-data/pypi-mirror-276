import colorcall
from setuptools import setup, find_packages

with open("/home/sw1mmer/projects/colorcall/colorcall/README.md") as file:
    long_description = file.read()

setup(
    name=colorcall.__name__,
    version=colorcall.__version__,
    author="Mikle Sedrakyan",
    description="Color call your caracal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sw1mmeR/colorcall/tree/main",
    packages=find_packages(),
    package_data={
        colorcall.__name__: ["py.typed"],
    },
    python_requires=">=3.11",
)
