#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/21.
# email to LipsonChan@yahoo.com
#
import os

from setuptools import setup, find_packages, Command

from NXSpider import version


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setup(
    name=version.__title__,
    version=version.__version__,
    author=version.__author__,
    author_email=version.__author_email__,
    url=version.__url__,
    description=version.__description__,
    license=version.__license__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mutagen",
        "terminaltables",
        "cryptography",
        "mongoengine",
        "requests",
        "colorama",
        "beautifulsoup4",
        "blinker",
        "cement",
    ],
    entry_points={
        "console_scripts": ["nxspider=NXSpider.bin.cli:main"]
    },
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['music', 'netease', 'cli', 'spider'],
    cmdclass={
        'clean': CleanCommand,
    },
)
