# setup.py
from setuptools import setup, find_packages

setup(
    name='crint',
    version='0.1.1',
    description='A simple module for colored terminal output',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Raj Krishnan',
    author_email='rajkrishnan.r@outlook.com',
    url='https://github.com/raj-krishnan-r/crint',  # Replace with your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
)
