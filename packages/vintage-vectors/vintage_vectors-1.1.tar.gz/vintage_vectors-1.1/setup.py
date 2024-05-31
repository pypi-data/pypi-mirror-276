from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
setup(
    name="vintage_vectors",
    version="1.1",
    packages=find_packages(),
    install_requires= [
        'torch'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)