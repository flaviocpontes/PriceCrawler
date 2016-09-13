from setuptools import setup
from codecs import open
from os import path

from crawler import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PriceCrawler',
    version=__version__,
    packages=['crawler'],
    install_requires=['lxml', 'cssselect'],
    license='MIT',
    author='Flávio Pontes',
    author_email='flaviocpontes@gmail.com',
    description='Crawls www.epocacosmeticos.com.br products',
    long_description=long_description,
)
