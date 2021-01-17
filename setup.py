import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "moodli",
    version = "0.1",
    author = "Jack Vanier",
    author_email = "jack.vanier16@outlook.com",
    description = ("A command line mood tracker."),
    license = "BSD",
    keywords = "mood tracker cli",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=find_packages(),
    scripts=["src/moodli"],
    long_description=read('README.md'),
    install_requires=[
        'tabulate',
        'pysftp',
    ]
)
