from setuptools import setup, find_packages

setup(
    name="up-bank-pyclient",
    version="0.1.0",
    description="Python client library for the UP Bank API",
    author="Jack Munro",
    author_email="jack@jsmunro.me",
    url="https://github.com/jackm43/up-bank-pyclient",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    include_package_data=True,
    license="GPL-3.0-or-later",
)