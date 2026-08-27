#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for PE BEAR."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pe-bear",
    version="2.0.0",
    author="PE BEAR Project",
    description="Professional PE file analyzer and editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PE-Manipulation-Tool",
    py_modules=["fichier_exe"],
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "pe-bear=fichier_exe:main",
        ],
    },
)
