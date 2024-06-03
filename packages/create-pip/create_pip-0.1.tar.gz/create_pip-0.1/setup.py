from setuptools import setup, find_packages

setup(
    name="create_pip",
    version = '0.1',
    packages=find_packages(),
    install_requies = [
        "numpy",
        "os",
        "time"
    ],
)