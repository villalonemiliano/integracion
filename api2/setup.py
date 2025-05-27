from setuptools import setup, find_packages

setup(
    name="api2",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "pydantic-settings",
        "aiosqlite",
    ],
) 