# pylint: disable=missing-docstring
import setuptools

NAME = "cmdparserkhv"

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name=NAME,
    version="0.0.0.9005",
    author="Arseniy Khvorov",
    author_email="khvorov45@gmail.com",
    description="Parses command line input",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/khvorov45/CmdParser",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "colorama"
    ]
)
