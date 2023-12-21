#!/bin/bash

set -ev

mkdir -p mycomponents

pytest

flake8;
sphinx-build -W -b html -qa -E docs docs/_build/html;
