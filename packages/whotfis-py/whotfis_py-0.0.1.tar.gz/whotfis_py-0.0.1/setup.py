from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Simple package to interact with the whois command line tool"
LONG_DESCRIPTION = "A simple package to interact with the whois command line tool without losing time in parsing"

setup(
    name="whotfis-py",
    version=VERSION,
    author="Valerio Pio De Nicola",
    author_email="valeriopio02@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'whois', 'whois command line', 'whois python', 'whois python package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ],
)