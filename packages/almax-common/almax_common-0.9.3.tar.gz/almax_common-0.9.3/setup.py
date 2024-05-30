from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='almax_common',
    version='0.9.3',
    description='A common library with some of my implementations',
    long_description='test',
    long_description_content_type='text/markdown',
    author='AlMax98',
    author_email='alihaider.maqsood@gmail.com',
    packages=find_packages(where='.'),  # Ensure it finds the Common package
    package_dir={'': '.'},  # Specify the root directory as the package directory
    install_requires=[],  # Add any dependencies here
);