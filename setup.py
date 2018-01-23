from setuptools import setup, find_packages
from os import path

import laboratory

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='laboratory',
    packages=find_packages(),
    version=laboratory.__version__,
    description="Sure-footed refactoring achieved through experimenting",
    long_description=long_description,
    author='Joe Alcorn',
    author_email='joealcorn123@gmail.com',
    url='https://github.com/joealcorn/laboratory',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    extras_require={
        'dev': [
            'Sphinx==1.6.6',
        ]
    },
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ]
)
