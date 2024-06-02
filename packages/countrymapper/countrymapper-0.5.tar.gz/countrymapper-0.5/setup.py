from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()
setup(
    name='countrymapper',
    version='0.5',
    description='A simple tool to normalise/standardise country names to their official country names or codes',
    long_description = long_description,
    long_description_content_type="text/markdown",
    author='Arfat Shaikh',
    packages=find_packages(),
)