from setuptools import setup, find_packages


file_descp = './README.md'
description = open(file_descp, "r").read()

setup(
    name='to_literal',
    version='v1.1.2',
    description='Librery to use it in a simple way to do a cast of an array to Literal[], to use it for validation with Pydantic',
    long_description=description,
    long_description_content_type='text/markdown',
    author='Adrià Martín Martorell',
    author_email='au7812ooae32@gmail.com',
    maintainer='Adrià Martín Martorell',
    maintainer_email='au7812ooae32@gmail.com',
    packages=find_packages()
)