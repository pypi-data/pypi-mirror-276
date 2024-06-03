import colorcall
from setuptools import setup, find_packages

with open("README.md") as file:
    long_description = file.read()

setup(
    name=colorcall.__name__,
    version=colorcall.__version__,
    author="Mikle Sedrakyan",
    author_email="scriptdefender@yandex.ru",
    description="Color call your caracal",
    include_package_data=True,
    license_files=("LICENSE",),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sw1mmeR/colorcall/tree/main",
    packages=find_packages(),
    package_data={
        colorcall.__name__: ["py.typed"],
    },
    python_requires=">=3.11",
)
