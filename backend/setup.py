from setuptools import find_packages, setup

setup(
    name="gym_management",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Your dependencies here
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.0",
        "pydantic>=1.8.0",
    ],
)
