from setuptools import setup, find_packages

setup(
    name='trajectory_compression',
    version='0.1.0',
    description='A Python library for compressing trajectories',
    packages=find_packages(), 
    install_requires=[
        'pandas',
        'geopandas',
        'matplotlib',
        'contextily',
        'shapely'
    ],
)
