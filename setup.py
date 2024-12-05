#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_tiehu
=================================================
"""

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="py3-tiehu",
    version="1.0.0",
    description="The Python3 Tiehu Library Developed By Guolei",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guolei19850528/py3_tiehu",
    author="guolei",
    author_email="174000902@qq.com",
    license="MIT",
    keywors=["tiehu", "铁虎", "停车", "智慧车场", "物管", "智慧社区"],
    packages=setuptools.find_packages('./'),
    install_requires=[
        "requests",
        "addict",
        "retrying",
        "jsonschema",
        "diskcache",
        "redis",
    ],
    python_requires='>=3.0',
    zip_safe=False
)