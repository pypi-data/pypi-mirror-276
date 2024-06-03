# setup.py
from setuptools import setup, find_packages

setup(
    name='harsha_hello_world',
    version='0.2',
    description='A simple Hello World package',
    author='Harsha',
    author_email='karampudi.sh@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'harsha-hello-world=harsha_hello_world.cli:greet',
        ],
    },
)
