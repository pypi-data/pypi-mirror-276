# setup.py
from setuptools import setup, find_packages

setup(
    name='allgraph',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'squarify'
    ],
    author='Arnav',
    author_email='arnav.singh7418@gmail.com',
    description='A library for creating various types of graphs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Arnav7418/AllGraph.py',  
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)

