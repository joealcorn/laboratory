from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='laboratory',
    packages=find_packages(),
    version='0.1.0',
    description='A place for experimenting',
    # long_description=long_description,
    author='Joe Alcorn',
    author_email='joealcorn123@gmail.com',
    url='https://github.com/joealcorn/laboratory',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',

    ]
)
