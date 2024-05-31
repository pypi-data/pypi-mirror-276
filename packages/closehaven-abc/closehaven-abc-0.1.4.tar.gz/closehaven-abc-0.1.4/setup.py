from setuptools import setup, find_packages

setup(
    name="closehaven-abc",
    version="0.1.4",
    packages=find_packages(),
    install_requires = [
        'fastapi==0.111.0',
        'pydantic==2.7.2',
        'azure-storage-blob==12.20.0'
    ]
)
