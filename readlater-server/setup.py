from setuptools import setup, find_packages

setup(
    name='ReadLater',
    version='0.5',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
)

