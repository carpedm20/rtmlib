from setuptools import find_packages, setup


def readme():
    with open("README.md", encoding="utf-8") as f:
        content = f.read()
    return content


def parse_requirements(fname="requirements.txt"):
    """Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file

    Returns:
        List[str]: list of requirements items

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
    """
    import re
    import sys
    from os.path import exists

    require_fpath = fname

    def parse_line(line):
        """Parse information from a line in a requirements text file."""
        if line.startswith("-r "):
            # Allow specifying requirements in other files
            target = line.split(" ")[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {"line": line}
            if line.startswith("-e "):
                info["package"] = line.split("#egg=")[1]
            elif "@git+" in line:
                info["package"] = line
            yield info

    def parse_require_file(fpath):
        with open(fpath, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info["package"]]
                item = "".join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


if __name__ == "__main__":
    setup(
        name="rtmlib",
        description="A library for real-time pose estimation.",
        author="Tau-J",
        author_email="taujiang@outlook.com",
        keywords="pose estimation",
        long_description=readme(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        include_package_data=True,
        url="https://github.com/Tau-J/rtmlib",
        license="Apache License 2.0",
        python_requires=">=3.7",
        install_requires=parse_requirements("requirements/runtime.txt"),
        extras_require={
            "all": parse_requirements("requirements.txt"),
            "optional": parse_requirements("requirements/optional.txt"),
        },
    )
