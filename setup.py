from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    long_description = read_me.read()


setup(
    name="repox",
    description="a lightweight Repox client written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    author="Mark Baggett",
    author_email="mbagget1@utk.edu",
    maintainer_email="mbagget1@utk.edu",
    url="https://github.com/markpbaggett/pyrepox",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
)