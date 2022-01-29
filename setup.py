from gettext import install
import os
from setuptools import setup

packageFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = packageFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name = 'pyreactor',
    url = 'https://github.com/Kyle-Gagnon-99/pyreactor',
    author = 'Kyle Gagnon',
    author_email = 'kmgagnon99@gmail.com',
    packages = ['pyreactor'],
    requires = install_requires,
    version = 'v1.0-SNAPSHOT',
    license = 'MIT',
    description = 'A python reactor library utilizing ZMQ',
    long_description = open('README.md').read()
)