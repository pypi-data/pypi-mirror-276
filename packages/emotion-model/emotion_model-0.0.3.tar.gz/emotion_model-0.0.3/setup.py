from pathlib import Path
from typing import List

from setuptools import find_packages, setup

# Package meta-data.
NAME = "emotion-model"
DESCRIPTION = "Emotion recognition package made with keras."
URL = "https://github.com/Ilyaant/emotion-clf-package"
EMAIL = "m1908142@edu.misis.ru"
AUTHOR = "Ilya Antonov & Paul Khoner"
REQUIRES_PYTHON = ">=3.6.0"

long_description = DESCRIPTION

# Load the package's VERSION file as a dictionary.
about = {}
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / "requirements"
PACKAGE_DIR = ROOT_DIR / "emotion_model"

with open(PACKAGE_DIR / "VERSION") as f:
    _version = f.read().strip()
    about["__version__"] = _version


def list_reqs(fname: str = "requirements.txt") -> List[str]:
    with open(REQUIREMENTS_DIR / fname) as fd:
        return fd.read().splitlines()


def get_long_description() -> str:
    base_dir = ROOT_DIR
    with (base_dir / "README.md").open(encoding="utf-8") as f:
        return f.read()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    package_data={"emotion_model": ["VERSION"]},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
