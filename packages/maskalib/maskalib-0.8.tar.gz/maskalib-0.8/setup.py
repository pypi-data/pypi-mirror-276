from setuptools import setup, find_packages

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='maskalib',
    version='0.8',
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
