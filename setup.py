#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

if __name__ == "__main__":
    here = os.path.abspath(".")
    README = open(os.path.join(here, 'README.md')).read()

    setup(
        name="py-auth-s",
        description="Authentication proxy for student projects",
        long_description=README,
        version='1.0.0',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        license="APL2",
        url="https://www.hs-heilbronn.de/win/studierende",
        maintainer="Detlef Stern",
        maintainer_email="detlef.stern@hs-heilbronn.de",
        keywords="education authorization",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Web Environment",
            "Intended Audience :: Education",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.7",
            "Topic :: Education",
        ],
        entry_points={
            'console_scripts': [
                'pyauths = py_auth_s:main',
            ],
        }
    )
