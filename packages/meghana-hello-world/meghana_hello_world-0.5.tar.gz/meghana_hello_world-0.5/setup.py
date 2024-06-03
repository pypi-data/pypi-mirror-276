# setup.py
from setuptools import setup, find_packages

setup(
    name='meghana_hello_world',
    version='0.5',
    description='A simple Hello World package with addition',
    author='meghana',
    author_email='meghanabl2112@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'meghana-hello-world=meghana_hello_world.cli:cli',
        ],
    },
)
