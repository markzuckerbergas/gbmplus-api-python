"""Setup script for gbmplus"""

import os.path
import re
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
PACKAGE_INIT = os.path.abspath(os.path.join('gbmplus', '__init__.py'))

with open(os.path.join(HERE, 'README.md')) as fid:
    README = fid.read()


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


__version__ = find_version(PACKAGE_INIT)


setup(
    name='gbmplus',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests', 'geocoder'],
    keywords=['gbmplus', 'gbmhomebroker', 'gbm'],
    description='GBM Plus API Python Library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/markzuckerbergas/gbmplus-api-python',
    author='markzuckerbergas',
    author_email='markzuckerbergas@protonmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)