"""
This files allows to install the package chaps_nats locally
===========================================================

@author: Pierre Dellenbach
"""

from setuptools import find_packages, setup

setup(
    name="chaps_nats",
    version="0.0.1",
    packages=find_packages("Src"),
    package_dir={"": "Src"},
)
