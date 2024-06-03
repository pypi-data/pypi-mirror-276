from setuptools import setup, find_packages
import os

# Wczytanie zawartości readme.md
with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyEclipse",
    version="0.1.0",
    author="SneakyFrameworkCreator",
    author_email="twoj_email@example.com",
    description="Krótki opis twojego projektu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twoj_github/nazwa_projektu",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    install_requires=[
        # tutaj wpisz wymagane biblioteki, np.
        # 'numpy',
        # 'requests',
    ],
)
