# Copyright (C) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in project root for information.
# The primary issue addressed in this build dependency resolution is: ModuleNotFoundError: No module named 'mmlspark.lightgbm._LightGBClassifier'

import os
from setuptools import setup, find_packages
import codecs
import os.path
import version

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

try:
    exec(open('version.py').read())
except IOError:
    print("Failed to load mmlspark version file for packaging. You must be in mmlspark root dir.",
          file=sys.stderr)
    sys.exit(-1)
VERSION = version.__version__

setup(
    name="miss__Lightgbm_mmlspark",
    version=VERSION,
    description="Microsoft ML for Spark",
    long_description="Microsoft ML for Apache Spark contains Microsoft's open source " +
                     "contributions to the Apache Spark ecosystem",
    license="MIT",
    packages=find_packages(),

    author="yongming.pang",
    author_email="891067464@qq.com",

    # Project's main homepage.
    url="https://github.com/Azure/mmlspark",

    classifiers=[
        "Programming Language :: Python :: 3"
    ],

    zip_safe=True,

    package_data={"mmlspark": ["../LICENSE.txt", "../README.txt"]}
)
