import pathlib
from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()
with open(
    str(pathlib.Path(__file__).parent.absolute()) + "/tiruka_fib_py/version.py", "r"
) as fh:
    version = fh.read().split("=")[1].replace("'", "")

setup(
    name="tiruka-fib-py",
    version=version,
    author="tiruka",
    author_email="tiruka.engineer@gmail.com",
    description="Calculates a Fibonacci number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiruka/fib-py",
    install_requires=["PyYAML>=4.1.2", "dill>=0.2.8"],
    extras_require={
        "server": ["Flask>=1.0.0"],
    },
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_require=">=3",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "fib-number = tiruka_fib_py.cmd.fib_numb:fib_numb",
        ]
    },
)
