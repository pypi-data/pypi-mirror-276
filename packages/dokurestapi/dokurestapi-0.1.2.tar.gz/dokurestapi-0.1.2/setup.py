from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

version = os.environ.get("VERSION")
if version is None:
    raise ValueError("VERSION environment variable not set.")

setup(
    name="dokurestapi",
    version=version,
    author="krowvin",
    author_email="charlie@krowvin.com",
    description="A Python package to interact with the DokuWiki REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krowvin/dokurestapi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    license="MIT",
)
