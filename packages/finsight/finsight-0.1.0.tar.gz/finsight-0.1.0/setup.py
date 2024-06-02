from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='finsight',
    version='0.1.0',  # Update this version number
    author='Ben Dawson',
    author_email='bjdawson1012@gmail.com',
    description='A package to provide financial insights from price data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BDaws04/finsight',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
