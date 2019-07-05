#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "numpy",
    "pandas",
    "scikit-learn",
    "scipy",
    "torch>=1.0",
    "torchvision",
    "tqdm",
    "umap",
    "aicsimageio>=0.6.3",
    # "fnet@git+https://github.com/AllenCellModeling/pytorch_fnet@master#egg=fnet",
]

setup_requirements = ["pytest-runner"]

test_requirements = [
    "pip>=19.0.3",
    "bumpversion>=0.5.3",
    "wheel>=0.33.1",
    "codecov",
    "coverage>=5.0a4",
    "Sphinx>=2.0.0b1",
    "sphinx_rtd_theme",
    "twine>=1.13.0",
    "pytest>=4.3.0",
    "pytest-cov>=2.6.1",
    "pytest-raises>=0.10",
    "pytest-runner>=4.4",
]

dev_requirements = [
    "altair",
    "black",
    "flake8",
    "jupyterlab",
    "matplotlib",
    "pre-commit",
    "scikit-learn",
    "tox",
]

extra_requirements = {
    "test": test_requirements,
    "setup": setup_requirements,
    "dev": dev_requirements,
    "all": test_requirements + setup_requirements + dev_requirements,
}

setup(
    author="Rory Donovan-Maiye",
    author_email="rorydm@alleninstitute.org",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: Allen Institute Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="translate brightfield images to and from FISH assay",
    entry_points={"console_scripts": []},
    install_requires=requirements,
    license="Allen Institute Software License",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="brightfield2fish",
    name="brightfield2fish",
    packages=find_packages(include=["brightfield2fish"]),
    python_requires=">=3.6",
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    extras_require=extra_requirements,
    url="https://github.com/AllenCellModeling/brightfield2fish",
    version="0.1.0",
    zip_safe=False,
)
