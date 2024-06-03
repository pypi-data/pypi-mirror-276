# setup.py
from setuptools import setup, find_packages

setup(
    name='hemanth-hello-world',
    version='0.4',
    description='A simple Hello World package',
    author='hemanth',
    author_email='hsbollina@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'hemanth-hello-world=hemanth_hello_world.cli:greet',
        ],
    },
)
