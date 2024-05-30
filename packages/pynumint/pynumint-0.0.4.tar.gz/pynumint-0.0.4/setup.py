import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynumint",                     # This is the name of the package
    version="0.0.4",                     # The initial release version
    author="Arjun Jagdale",              # Full name of the author
    author_email="arjunjagdale14@gmail.com",  # Author's email address
    description="pynumint Test Package for Numerical Integration Demo",
    long_description=long_description,   # Long description read from the readme file
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/pynumint/",  # URL of the project
    packages=setuptools.find_packages(), # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                   # Information to filter the project on PyPi website
    python_requires='>=3.6',             # Minimum version requirement of the package
    py_modules=["pynumint"],             # Name of the python package
    package_dir={'': 'pynumint/src'},    # Directory of the source code of the package
    install_requires=[]                  # Install other dependencies if any
)
