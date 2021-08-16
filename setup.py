from setuptools import setup

setup(
    name="msys",
    install_requires=[
        "pymsys>=0.0.3"
        "numpy~=1.20.2",
        "pyparsing~=2.4.7",
        "requests",
        "setuptools~=56.0",
        "fastapi~=0.65",
        "uvicorn~=0.13",
        "click~=7.0",
    ],
    extras_require={
        'test': "pytest~=6.2.3",
    },
)
