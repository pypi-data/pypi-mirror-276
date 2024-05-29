from setuptools import setup, find_packages
import os

def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

setup(
    name='visible-to-sqlite',
    author='Avner Shanan',
    version='1.0.0',
    description="Convert exported CSV from Visible app to a SQLite DB",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'sqlite-utils'
    ],
    entry_points={
        'console_scripts': [
            'visible-to-sqlite = visible_to_sqlite.cli:cli',
        ],
    },
)