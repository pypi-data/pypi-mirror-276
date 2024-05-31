#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="exobject",
    version=0.9,
    description=("Extend Object Code"),
    long_description=open("README.rst").read(),
    author="LenShang",
    author_email="lenshang@qq.com",
    maintainer="LenShang",
    maintainer_email="lenshang@qq.com",
    license="BSD License",
    packages=find_packages(),
    platforms=["all"],
    url="",
    install_requires=["python-dateutil", "parsel"],
)
