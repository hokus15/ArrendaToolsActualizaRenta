# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import pkg_resources

__version__ = "0.0.0"

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('LICENSE', encoding='utf-8') as f:
    license = f.read()

with open('requirements.txt') as f:
    install_requires = [str(r) for r in pkg_resources.parse_requirements(f)]


setup(
    name='arrendatools_ipc',
    version=__version__,
    description='Módulo de Python que realiza la actualización de rentas de alquiler por anualidades completas con el IPC (LAU) descrita en la web del INE de España. ',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/hokus15/ArrendaToolsIPC',
    author='hokus15',
    author_email='hokus@hotmail.com',
    packages=find_packages(exclude=('tests', '.vscode', '.github')),
    license=license,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
