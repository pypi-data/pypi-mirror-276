# setup.py
from setuptools import setup, find_packages

setup(
    name="romyai",
    version="0.2.0",
    author="Md Rehan",
    author_email="mdrehan4all@gmail.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mdrehan4all/romyai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)