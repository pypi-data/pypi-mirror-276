from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first Python package <tutorial>'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
    name="afnaan",
    version=VERSION,
    author="Abdulbasit Alabi",
    author_email="abdulbasitdamilola6@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['setuptools', 'wheel'],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)