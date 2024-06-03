import loggissimo
from setuptools import setup, find_packages

with open("README.md") as file:
    long_description = file.read()

setup(
    name=loggissimo.__name__,
    version=loggissimo.__version__,
    author="MikleSedrakyan & AfanasevAndrey",
    author_email="scriptdefender@yandex.ru",
    description="Awesome and simple logger",
    license_files=("LICENSE",),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sw1mmeR/loggissimo/tree/main",
    packages=find_packages(),
    package_data={
        loggissimo.__name__: ["py.typed"],
    },
    install_requires=[
        "colorcall>=0.2.1",
    ],
    tests_require=[
        "pytest==7.4.0",
    ],
    python_requires=">=3.11",
)
