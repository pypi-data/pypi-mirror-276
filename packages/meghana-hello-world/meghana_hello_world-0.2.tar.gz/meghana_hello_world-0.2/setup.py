# setup.py
from setuptools import setup, find_packages

setup(
    name='meghana_hello_world',
    version='0.2',
    description='A simple Hello World package',
    author='meghana',
    author_email='meghanabl2112@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'meghana-hello-world=meghana_hello_world.cli:greet',
        ],
    },
)
