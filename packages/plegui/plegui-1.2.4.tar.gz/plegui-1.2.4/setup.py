from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="plegui",
    version="1.2.4",
    description="A library used to make GUIs and Messages boxes and other..",
    long_description=README,
    long_description_content_type="text/markdown",
    author="PyGaps CEO",
    author_email="soqratiakram33@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
