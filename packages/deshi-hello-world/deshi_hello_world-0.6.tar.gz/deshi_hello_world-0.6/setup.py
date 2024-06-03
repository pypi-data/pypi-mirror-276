# setup.py
from setuptools import setup, find_packages

setup(
    name='deshi_hello_world',
    version='0.6',
    description='A simple hello world package with multiplication functionality',
    author='deshi',
    author_email='deshithabollina28@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'deshi-greet=hello_world.cli:greet',
            'deshi-multiply=hello_world.cli:multiply_command',
        ],
    },
)
