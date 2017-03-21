#!/bin/bash

# builds our packages for pypi

source env/bin/activate
pip install -r requirements.txt

echo "Removing any previous build dir..."
rm -rf build
echo "Removing any previous dist dir..."
rm -rf dist

echo "Building for python 2.x..."
python setup.py sdist bdist_wheel
echo "Building for python 3.x..."
/usr/local/bin/python3.5 setup.py sdist bdist_wheel

echo "Running twine upload..."
twine upload dist/*
