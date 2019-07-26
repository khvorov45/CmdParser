# pylint: disable=missing-docstring
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="cmdparser-khvorov45",
    version="0.0.1",
    author="Arseniy Khvorov",
    author_email="khvorov45@gmail.com",
    description="Parses command line input",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/khvorov45/cdmparser",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
