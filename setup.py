from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    long_description = read_me.read()


setup(
    name="repox",
    description="a lightweight Repox client written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.3",
    author="Mark Baggett",
    author_email="mbagget1@utk.edu",
    maintainer_email="mbagget1@utk.edu",
    url="https://github.com/markpbaggett/pyrepox",
    packages=find_packages(),
    install_requires=["requests>=2.2.1", "xmltodict>=0.11.0", "arrow>=0.13.0"],
    extras_require={
        "docs": [
            "sphinx >= 1.4",
            "sphinxcontrib-napoleon >= 0.7",
            "recommonmark >= 0.4.0",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    keywords=["libraries", "dpla", "europeana", "aggregators"],
)
