from setuptools import setup, find_packages

setup(
    name="create_pip",
    version = '0.2',
    packages=find_packages(),
    install_requies = [
        "numpy",
        "os",
        "time"
    ],
    entry_points = {
        "console_scripts" : [
            "create_pip = create_pip:make_folder",
        ],
    },
)