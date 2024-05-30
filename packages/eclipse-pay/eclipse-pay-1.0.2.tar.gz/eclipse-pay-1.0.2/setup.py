from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'Manage payments on scratch automatically.'

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="eclipse-pay",
    version=VERSION,
    author="LIZARD_OFFICIAL",
    author_email="<lizard.official.77@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=["python", "scratch","scratch.mit.edu","Blockbit","LRCOIN","BB","LRC","eclipseai"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["scratchattach==1.7.3","requests==2.27.1"]
)