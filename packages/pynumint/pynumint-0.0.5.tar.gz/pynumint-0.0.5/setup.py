import setuptools

# Display a message during installation
print("Installing pynumint...")

def print_word_star_pattern(word):
    # Dictionary containing the star patterns for each letter
    letter_patterns = {
        'p': [
            "***** ",
            "*    *",
            "*    *",
            "***** ",
            "*     ",
            "*     ",
            "*     "
        ],
        'y': [
            "*   * ",
            "*   * ",
            " * *  ",
            "  *   ",
            "  *   ",
            "  *   ",
            "  *   "
        ],
        'n': [
            "*   * ",
            "**  * ",
            "* * * ",
            "*  ** ",
            "*   * ",
            "*   * ",
            "*   * "
        ],
        'u': [
            "*   * ",
            "*   * ",
            "*   * ",
            "*   * ",
            "*   * ",
            "*   * ",
            "***** "
        ],
        'm': [
            "*   * ",
            "** ** ",
            "* * * ",
            "* * * ",
            "*   * ",
            "*   * ",
            "*   * "
        ],
        'i': [
            " ***  ",
            "  *   ",
            "  *   ",
            "  *   ",
            "  *   ",
            "  *   ",
            " ***  "
        ],
        't': [
            "***** ",
            "  *   ",
            "  *   ",
            "  *   ",
            "  *   ",
            "  *   ",
            "  *   "
        ]
    }
    
    # Iterate over each letter in the word
    for line_index in range(7):
        # Iterate over each letter in the word
        for letter in word:
            # Print the corresponding pattern for the letter
            print(letter_patterns[letter.lower()][line_index], end='  ')
        print()  # Move to the next line after printing each row of letters

# Example usage
print_word_star_pattern('PYNUMINT')

print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynumint",
    version="0.0.5",
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
)

# Print a completion message
print("pynumint has been successfully installed!")
