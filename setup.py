from gettext import install
from setuptools import setup

setup(
    name = 'pyreactor',
    url = 'https://github.com/Kyle-Gagnon-99/pyreactor',
    author = 'Kyle Gagnon',
    author_email = 'kmgagnon99@gmail.com',
    packages = ['pyreactor'],
    requires = [
        'pyzmq',
        'protobuf'
        ],
    version = 'v1.0-SNAPSHOT',
    license = 'MIT',
    description = 'A python reactor library utilizing ZMQ',
    long_description = open('README.md').read()
)