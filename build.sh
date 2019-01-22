#!/bin/bash

set -ev

if [ "`python -V 2>&1`" == "Python 2.6.9" ]; then 
    cp .collections.py /home/travis/virtualenv/python2.6.9/lib/python2.6/collections.py
fi

py.test

flake8;
sphinx-build -W -b html -qa -E docs docs/_build/html;

