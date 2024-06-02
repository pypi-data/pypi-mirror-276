from setuptools import setup, find_packages

setup(
    name="ajvpy2",
    version="0.1.0",
    author="Anthony Chadwick",
    description="A thin wrapper around the AJV JSON Validator for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/atchad/ajvpy2",
    packages=find_packages(exclude=["tests*", "examples*"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "mini-racer>=0.12.3",
        "pytest>=6.0.0",
    ],
    extras_require={
        "dev": [
            "flake8",
            "black",
        ],
    },
    entry_points={
        "console_scripts": [
            "ajvpy2=ajvpy2.__main__:main",
        ],
    },
)
