# -*- coding: utf-8 -*-
"""
Created on 2020/4/22 10:45 PM
---------
@summary:
---------
@author: Boris
@email: boris@bzkj.tech
"""

from os.path import dirname, join
from sys import version_info

import setuptools

if version_info < (3, 0, 0):
    raise SystemExit("Sorry! jmpy requires python 3.0.0 or later.")


with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="iac-inscript",
    version='1.0.1',
    author="Boris",
    license="MIT",
    author_email="boris@bzkj.tech",
    description="python代码一键加密",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Cython==3.0.10"],
    entry_points={"console_scripts": ["iac-inscript = inscript.cmdline:execute"]},
    url="https://github.com/Khalil12138/iac-inscript.git",
    packages=packages,
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
