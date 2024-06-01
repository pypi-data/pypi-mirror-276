import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ellipsisPySpark",
    version="0.0.0",
    author="Daniel van der Maas",
    author_email="daniel@ellipsis-drive.com",
    description="Package to load Ellipsis raster and vector layers as pySpark DataFrames.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ellipsis-drive/pySpark",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
    'pandas',
    'numpy',
    'json',
    'pyspark',
    'ellipsis',
    'math'
    ],
    python_requires='>=3.6',
)
