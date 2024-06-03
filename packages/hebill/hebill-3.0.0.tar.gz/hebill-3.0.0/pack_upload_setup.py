# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='hebill',
    version='3.0.0',
    description='Hebill Python Library',
    long_description=open(r'README.MD', encoding='utf-8').read(),
    long_description_content_type='text/plain',
    packages=find_packages(),
    package_data={
        '': ['*.md', '*.MD'],
    },
    install_requires=[
        'colorama==0.4.6',
    ],
    python_requires='>=3.12',
)
