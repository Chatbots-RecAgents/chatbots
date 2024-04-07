from setuptools import setup, find_packages
from pathlib import Path

# Read version from __init__.py
here = Path(__file__).absolute().parent
version_data = {}
with open(here.joinpath("chatlib", "__init__.py"), "r") as f:
    exec(f.read(), version_data)
version = version_data.get("__version__", "0.0")

# Define dependencies
install_requires = [
    "numpy>=1.19",
    "pandas>1.0.3,<2",
    # Add the rest of the dependencies later (check with the team)
]

setup(
    name="chatlib",
    version=version,
    install_requires=install_requires,
    package_dir={"": "."},
    python_requires=">=3.6, <3.12",
    packages=find_packages(where=".", exclude=["docs", "examples", "tests"]),
    include_package_data=True,
)
