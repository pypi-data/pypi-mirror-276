"""
Multi-object Tracking (MOT) for perceptionn OD(Obstacle Detection), used for overall evaluation of
E2E Tracking system.

Author: Haokun Zhang <haokun.zhang@hirain.com>
Copyright: Haokun Zhang (c)
"""

from setuptools import setup, find_packages

_REQS = None

def _get_package_name():
    _name = None
    with open("./odmetrics/_internal/_configs.py") as f:
        res = [line.strip() for line in f.readlines()]
        for line in res:
            if line.startswith("__name__"):
                _name = line.split()[-1].strip('"')
                break

    if _name is None:
        raise ReferenceError("Could not find package name.")
    return _name


def _get_package_version():
    _version = None
    with open("./odmetrics/_internal/_configs.py") as f:
        res = [line.strip() for line in f.readlines()]
        for line in res:
            if line.startswith("_VERSION_RELEASED"):
                _version = line.split()[-1].strip('"')
                break

    if _version is None:
        raise ReferenceError("Could not find package version.")
    return _version


def _get_dependencies():
    _req = None
    with open("requirements.txt") as f:
        _req = f.read().splitlines()

    if _req is None:
        raise ReferenceError("Could not find package dependencies.")
    return _req


def _get_long_description():
    _ld = None
    with open("./README.md", encoding="utf-8") as f:
        _ld = f.read()

    if _ld is None:
        raise ReferenceError("Could not load long description.")
    return _ld



setup(
    name=_get_package_name(),
    version=_get_package_version(),
    packages=find_packages(include=["odmetrics*"]),
    include_package_data=True,
    description="Multi-object Tracking (MOT) for perceptionn OD(Obstacle Detection), used for overall evaluation of E2E Tracking system.",
    author="Haokun Zhang",
    author_email="haokun.zhang@hirain.com",
    license="GNU General Public License v3 (GPLv3)",
    install_requires=_get_dependencies(),
    long_description=_get_long_description(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7"
)
