from setuptools import setup
from io import open





ld = open("README1.md",encoding="utf-8").read()


setup(
    name='voxelworldapi',
    version='1.0.1',
    packages=['voxelworldapi'],
    install_requires=['requests'],
    author='CallFish',
    author_email='callfish@mail.ru',
    description='A Python library for interacting with VoxelWorld API',
    url='https://github.com/callfishxt/voxelworldapi',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=ld
)

