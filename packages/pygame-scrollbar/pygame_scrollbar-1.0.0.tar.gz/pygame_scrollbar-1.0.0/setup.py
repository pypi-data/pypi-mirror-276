from setuptools import setup, find_packages

VERSION = '1.0.0'
NAME = "pygame_scrollbar"
AUTHOR = "FrickTzy (Kurt Arnoco)"
DESCRIPTION = 'A package for adding scrollbar to surfaces in pygame.'

with open("README.md", "r") as file:
    long_description = file.read()

URL = 'https://github.com/FrickTzy/Pygame-Scrollbar'

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url=URL,
    keywords=['python', 'pygame', 'python game', 'python game development',
              'scrollbar in pygame', 'python scrollbar', 'pygame scrollbar'],
)