#!/usr/bin/env python3
"""
Setup script for Quantum Randomness Service.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quantum-randomness-service",
    version="1.0.0",
    author="Anshuman Shukla",
    author_email="anshuman.contact07@gmail.com",
    description="A service providing true quantum random numbers from ANU QRNG and other sources",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/07anshuman/quantum-randomness-service",
    packages=find_packages(include=["app", "qrandom"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "redis": [
            "redis>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "quantum-randomness-service=app.main:main",
            "qrandom=app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "app": ["*.py", "*.md"],
    },
    keywords="quantum random number generator qrng anu api service",
    project_urls={
        "Bug Reports": "https://github.com/07anshuman/quantum-randomness-service/issues",
        "Source": "https://github.com/07anshuman/quantum-randomness-service",
        "Documentation": "https://github.com/07anshuman/quantum-randomness-service#readme",
    },
) 
