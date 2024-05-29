# setup.py

from setuptools import setup, find_packages

setup(
    name='iotics_auth',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'requests',
        'iotics-identity',
        'iotics-grpc-client', 
    ],
    author='gaurav ms',
    author_email='datascientist.msgaurav@gmail.com',
    description='A library for IOTICS identity management',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
