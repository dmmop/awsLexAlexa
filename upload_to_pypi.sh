#!/bin/bash

#install from test
#------------------
#pip install -i https://test.pypi.org/simple/ awsLexAlexa
#
#
rm -r awsLexAlexa.egg-info
rm -r dist
python3 setup.py sdist

#upload to test
#----------------
#python3 -m twine upload -r testpypi dist/$(ls dist)

#upload to production
#-----------------------
python3 -m twine upload dist/$(ls dist)
