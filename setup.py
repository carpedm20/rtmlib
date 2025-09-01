from setuptools import find_packages, setup


def readme():
    with open("README.md", encoding="utf-8") as f:
        content = f.read()
    return content


# --- FIX 1: Add back the correct get_version function ---
version_file = "rtmlib/version.py"


def get_version():
    with open(version_file, "r") as f:
        exec(compile(f.read(), version_file, "exec"))
    import sys

    # return short version for sdist
    if "sdist" in sys.argv or "bdist_wheel" in sys.argv:
        return locals()["short_version"]
    else:
        return locals()["__version__"]


# --- FIX 2: Use the full, correct parse_requirements function ---
def parse_requirements(fname="requirements.txt", with_version=True):
    """Parse the package dependencies listed in a requirements file."""
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
            else:
                # This is the crucial part you were missing
                pat = "(" + "|".join([">=", "==", ">"]) + ")"
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]
                info["package"] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    if ";" in rest:
                        version, platform_deps = map(str.strip, rest.split(";"))
                        info["platform_deps"] = platform_deps
                    else:
                        version = rest
                    info["version"] = (op, version)
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
                if with_version and "version" in info:
                    parts.extend(info["version"])
                if not sys.version.startswith("3.4"):
                    platform_deps = info.get("platform_deps")
                    if platform_deps is not None:
                        parts.append(";" + platform_deps)
                item = "".join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


if __name__ == "__main__":
    setup(
        name="rtmlib",
        version=get_version(),
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
