import colorcall
from setuptools import setup, find_packages

setup(
    name=colorcall.__name__,
    version=colorcall.__version__,
    author="Mikle Sedrakyan",
    description="Color call your caracal",
    packages=find_packages(),
    package_data={
        colorcall.__name__: ["py.typed"],
    },
)
