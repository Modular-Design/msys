from setuptools import setup

setup(
    name="msys",
    install_requires=[
        "numpy~=1.20.2",
        "pyparsing~=2.4.7",
        "setuptools~=56.0",
        "fastapi~=0.65",
        "uvicorn~=0.13",
        "click~=7.0",
    ],
    extra_require={
        "pytest~=6.2.3",
    },
)
