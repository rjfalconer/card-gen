#!/usr/bin/env python
"""Setup script for card-gen package."""

from setuptools import setup, find_packages

setup(
    name="card-gen",
    version="2.0.0",
    description="A tool to generate images of Poker playing cards",
    author="Richard Falconer",
    author_email="rjfalconer@users.noreply.github.com",
    url="https://github.com/rjfalconer/card-gen",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Wand>=0.6.13",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)