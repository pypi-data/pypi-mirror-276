import setuptools

# Display a message during installation
print("Installing pynumint...")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynumint",
    version="0.0.7",
    author="Arjun Jagdale",
    author_email="arjunjagdale14@gmail.com",
    description="pynumint Test Package for Numerical Integration Demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/pynumint/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["pynumint"],
    package_dir={'': 'pynumint/src'},
    install_requires=[],

    entry_points={
        'console_scripts': [
            'pynumint-post-install = post_install:print_word_star_pattern',
        ],
    },
)

# Print a completion message
print("pynumint has been successfully installed!")
