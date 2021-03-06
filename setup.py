"""rhodes."""
import io
import os
import re

from setuptools import find_packages, setup

VERSION_RE = re.compile(r"""__version__ = ['"]([0-9b.]+)['"]""")
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*args):
    """Read complete file contents."""
    return io.open(os.path.join(HERE, *args), encoding="utf-8").read()


def get_version():
    """Read the version from this module."""
    init = read("src", "rhodes", "__init__.py")
    return VERSION_RE.search(init).group(1)


def get_requireemnts():
    """Read the requirements file."""
    raw_requirements = read("requirements.txt")
    requirements = []
    dependencies = []

    for req in raw_requirements.splitlines():
        req = req.strip()
        if not req:
            continue

        if req.startswith("#"):
            continue

        if "+" in req:
            dependencies.append(req)
        else:
            requirements.append(req)

    return requirements, dependencies


INSTALL_REQUIRES, DEPENDENCY_LINKS = get_requireemnts()

setup(
    name="rhodes",
    version=get_version(),
    packages=find_packages("src"),
    # TODO: Collect these with os.walk
    package_data={"rhodes": ["py.typed", "*.pyi"], "rhodes.states": ["*.pyi"], "rhodes.states.services": ["*.pyi"]},
    package_dir={"": "src"},
    url="https://github.com/mattsb42/rhodes",
    author="Matt Bullock",
    author_email="m@ttsb42.com",
    maintainer="Matt Bullock",
    description="rhodes",
    long_description=read("README.rst"),
    keywords="rhodes rhodes",
    data_files=["README.rst", "CHANGELOG.rst", "LICENSE", "requirements.txt"],
    license="Apache 2.0",
    install_requires=INSTALL_REQUIRES,
    dependency_links=DEPENDENCY_LINKS,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
