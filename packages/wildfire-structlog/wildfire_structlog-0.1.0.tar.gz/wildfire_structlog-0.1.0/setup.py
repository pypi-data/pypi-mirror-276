from setuptools import setup, find_packages

setup(
    name='wildfire_structlog',
    version='0.1.0',
    description='A structlog library for wildfire',
    author='Jie Shen',
    author_email='jshen@paloaltonetworks.com',
    packages=find_packages(),
    install_requires=[
        'structlog==24.1.0',
        'orjson==3.10.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)