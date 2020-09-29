import os
from glob import glob
from setuptools import setup, find_packages


setup(
    name='atm',
    version='0.1dev',
    description='TBA',
    author='Afsoon Afzal',
    author_email='afsoona@cs.cmu.edu',
    url='https://github.com/afsafzal/atm-controller-challenge',
    license='mit',
    python_requires='>=3.6',
    install_requires = [
        'pytest==4.4.0',
        'pexpect==4.6.0',
        'attrs==19.1.0',
        'pyyaml==5.1',
    ],
    packages = [
        'atm'
    ]
)
