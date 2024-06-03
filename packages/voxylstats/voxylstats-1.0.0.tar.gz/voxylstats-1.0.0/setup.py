from setuptools import setup, find_packages
import pathlib


HERE = pathlib.Path(__file__).parent
with open(f"{HERE}/README.md") as f:
    README = f.read()



setup(
    name='voxylstats',
    version='1.0.0',
    description='A simple python wrapper for the Voxyl API',
    long_description=README,
    author='_lightninq & firestarad',
    license='MIT'
)

