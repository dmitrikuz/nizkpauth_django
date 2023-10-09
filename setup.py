from setuptools import find_packages, setup

setup(
    name='nizkpauth_django',
    version='1.0',
    packages=find_packages(),
    install_requires=['django>=4.2.6', 'djangorestframework>=3.14.0', 'nizkpauth>=1.0.0']
)