from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readMe = fh.read();

with open("requirements.txt") as f:
    required = f.read().splitlines();

setup(
    name='almax_common',
    version='0.9.6',
    description='A common library with some of my implementations',
    long_description=readMe,
    long_description_content_type='text/markdown',
    author='AlMax98',
    author_email='alihaider.maqsood@gmail.com',
    packages=find_packages(),
    package_dir={'': '.'},
    install_requires=required,
);