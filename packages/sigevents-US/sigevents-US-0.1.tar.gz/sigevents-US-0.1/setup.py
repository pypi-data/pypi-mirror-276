# setup.py

from setuptools import setup, find_packages

setup(
    name="sigevents-US",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    author="Syed",
    author_email="snaqvi@davincistudio.org",
    description="A package to add significant US events to a dataset",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/H-Naq/sigevents-US",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
