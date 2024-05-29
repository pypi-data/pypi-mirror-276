from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simplecalculatorpaulit",  # Replace with your own username
    version="1.0.0",
    author="Paulius Litvinas",
    author_email="paulit@ktu.lt",
    description="A simple calculator module for arithmetic, scientific, and statistical operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulit00/simplecalculatorpaulit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)