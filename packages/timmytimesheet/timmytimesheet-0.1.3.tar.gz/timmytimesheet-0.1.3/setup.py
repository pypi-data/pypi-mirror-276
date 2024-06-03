import os
from setuptools import setup, find_packages

def get_install_requires() -> list[str]:
    """
    Returns requirements.txt parsed to a list
    """
    fname = 'requirements.txt'
    targets = []

    with open(fname, 'r') as f:
        targets = f.read().splitlines()

    return targets

setup(
        name = "timmytimesheet",
        version = "0.1.3",
        description = "a basic timesheeting cli",
        author="jumper385 (Henry Chen)",
        install_package_data=True,
        install_requires = get_install_requires(),
        packages = find_packages(),
        keywords = ["timesheeting"],
        entry_points = {
            'console_scripts': [
                'timmy=timmy.main:app']},
            classifiers = [
                'Programming Language :: Python :: 3',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                ])

