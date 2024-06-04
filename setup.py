from setuptools import find_packages, setup

setup(
    name='package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # any dependencies, if you have them
        'networkx',
        'osmnx',
        'matplotlib',
        'geopy',
        'tk',
        'geopandas',
        ],
)

