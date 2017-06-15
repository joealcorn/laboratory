from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='laboratory',
    packages=find_packages(),
    version='0.4.2',
    description="A Python port of Github's Scientist lib.",
    long_description=long_description,
    author='Joe Alcorn',
    author_email='joealcorn123@gmail.com',
    url='https://github.com/joealcorn/laboratory',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
