from setuptools import setup, find_packages
from os import path
working_dir = path.abspath(path.dirname(__file__))

with open(path.join(working_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="lognition",
    version="0.0.3",
    author="Abtin Turing",
    description="Log everything in style.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "coloredlogs",
        "verboselogs",
        "yaspin"
    ]
)
