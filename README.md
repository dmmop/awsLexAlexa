Long description about de module (Custom)

compile: python setup.py sdist --formats=gztar,zip
install with: python setup.py install --record files_aws.txt
uninstall: cat files_aws.txt | xargs sudo rm -rf
