from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tiruka-fib-py",
    version="0.0.1",
    author="tiruka",
    author_email="tiruka.engineer@gmail.com",
    description="Calculates a Fibonacci number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiruka/fib-py",
    install_requires=[],
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
