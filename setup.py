from setuptools import setup, find_packages
from codecs import open
from os import path


HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tf2-utilities",
    version="0.3.4",
    description="Get information about TF2 items, effects, skins and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j0hnnyblack/python-tf2-utilities",
    author="Johnny Black",
    author_email="lokedixon@hotmail.my",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["tf2utilities"],
    include_package_data=True,
    install_requires=['requests', 'vdf'],
    keywords=["tf2", "teamfortress2", "steam", "trade", "trading"]
)
