from setuptools import setup, find_packages
from directedit import version
setup(
    name='directedit',
    version=version,
    author='Monsler',
    description='Lightweight managing folder contents library',
    author_email='galileoru22@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

)
