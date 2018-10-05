#!/usr/bin/env python

from setuptools import setup

with open("README.md" "r") as fh:
    long_description = fh.read()

setup(name="Quince",
      version="1.0",
      description="Classic Spanish card game.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Dan Liberatori",
      author_email="daniel.liberatori@gmail.com",
      url="http://www.danliberatori.com",
      packages=["quince", "ui"]
      )
