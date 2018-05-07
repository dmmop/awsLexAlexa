#AwsLexAlexa [![Generic badge](https://img.shields.io/badge/Python-3.6-green.svg)](https://shields.io/)![Travis](https://img.shields.io/travis/USER/REPO.svg)

This library may wrap the internal logistic between Amazon Lex or Alexa (Amazon echo) using AWS Lambda as background serverless.

You can see the implementation in `lambda_function.py`

**Compile:** 
```bash
python setup.py sdist --formats=gztar,zip
```
**Install**: 
```bash
python setup.py install --record files_aws.txt
```
**Uninstall**: 
```bash
cat files_aws.txt | xargs sudo rm -rf
```

