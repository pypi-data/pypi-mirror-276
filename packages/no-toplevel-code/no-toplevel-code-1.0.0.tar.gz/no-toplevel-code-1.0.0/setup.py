import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="no-toplevel-code",
    version="1.0.0",
    author="Kavi Gupta",
    author_email="kavig+no_toplevel_code@mit.edu",
    description="Wrap and unwrap code to allow for modules without top-level code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/no-toplevel-code",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[],
)
