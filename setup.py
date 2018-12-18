"""Setup KEP.py"""
from codecs import open
from os import path
from setuptools import setup, find_packages

HERE = path.dirname(path.realpath(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='keppy',
    version='0.0.3',
    install_requires=['Enum34'],
    description='A Python parser of Kepware projects',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/jmbeach/KEP.py',
    author='jmbeach',
    author_email='jaredbeachdesign@gmail.com',
    keywords='kepware parser',
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
