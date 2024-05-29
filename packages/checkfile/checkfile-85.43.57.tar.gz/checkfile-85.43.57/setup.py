from setuptools import setup, find_packages

setup(
    name='checkfile',
    version='85.43.57',
    description='A Python package that stops files from being edited.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='JZ Enterprises',
    packages=find_packages(),  # Automatically find packages in the current directory
    python_requires='>=3.6',
)
