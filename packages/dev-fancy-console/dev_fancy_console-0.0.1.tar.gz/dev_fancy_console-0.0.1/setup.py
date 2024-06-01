from setuptools import setup, find_packages
from os.path import join, abspath, dirname

def read(*pathcomponents):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), *pathcomponents)) as thefile:
        return thefile.read()

setup(
    name='dev_fancy_console',
    version='0.0.1',
    description='Stylized Python console, a project made for fun',
    author="SKoprek",
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    url='https://github.com/SKoprek/python-fancy-console',
    entry_points={
        "console_scripts": [
            "fancy_example_1 = dev_fancy_console.examples:example_1",
            "fancy_example_2 = dev_fancy_console.examples:example_2",
            "fancy_example_3 = dev_fancy_console.examples:example_3",
            "fancy_example_4 = dev_fancy_console.examples:example_4",
        ]
    }
)
