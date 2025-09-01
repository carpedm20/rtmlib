import re
import os

from setuptools import find_packages, setup


def _load_req(path: str):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


requirements = _load_req("requirements.txt")

_REQ_PATTERN = re.compile(r"^requirements-(\w+)\.txt$")
_REQ_BLACKLIST = {"zoo", "test"}
group_requirements = {
    item.group(1): _load_req(item.group(0))
    for item in [_REQ_PATTERN.fullmatch(reqpath) for reqpath in os.listdir()]
    if item
    if item.group(1) not in _REQ_BLACKLIST
}

setup(
    name="rtmlib",
    packages=find_packages(),
    version="0.0.1",
    install_requires=requirements,
    tests_require=(group_requirements.get("test") or []),
    extras_require=group_requirements,
    dependency_links=["git+https://github.com/deepghs/waifuc.git@main#egg=waifuc"],
)
