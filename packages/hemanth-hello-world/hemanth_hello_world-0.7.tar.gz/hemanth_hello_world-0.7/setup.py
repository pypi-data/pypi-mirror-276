# setup.py

from setuptools import setup, find_packages

setup(
    name='hemanth_hello_world',
    version='0.7',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies if required
    ],
    entry_points={
        'console_scripts': [
            'subtract=hemanth_hello_world.cli:main',
        ],
    },
    description='A simple package to subtract two numbers',
    author='Hemanthbollina123',
    author_email='hsbollina@example.com',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
