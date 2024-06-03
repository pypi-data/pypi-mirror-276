# setup.py
from setuptools import setup, find_packages

setup(
    name='deshi_hello_world',
    version='0.1',
    description='A simple Hello World package',
    author='deshi',
    author_email='deshithabollina28@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'deshi-hello-world=deshi_hello_world.cli:greet',
        ],
    },
)

