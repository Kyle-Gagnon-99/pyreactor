from setuptools import setup

setup(
    name = 'pyreactor',
    url = 'https://github.com/Kyle-Gagnon-99/pyreactor',
    author = 'Kyle Gagnon',
    author_email = 'kmgagnon99@gmail.com',
    packages = ['pyreactor'],
    install_requires = ['pyzmq', 'protobuf'],
    version = 'v1.0.0',
    license = 'MIT',
    description = 'A python reactor library utilizing ZMQ',
    long_description = open('README.md').read()
)