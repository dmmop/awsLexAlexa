# AwsLexAlexa  [![Generic badge](https://img.shields.io/badge/Python-3.4,%203.5,%203.6-green.svg)](https://shields.io/)

This library may wrap the internal logistic between Amazon Lex or Alexa (Amazon echo) using AWS Lambda as background serverless.

You can see the implementation in `lambda_function.py`.

**Usage:**
```python
from awsLexAlexa.event_handler import EventHandler, LEX, ALEXA

ev = EventHandler()
logger = ev.get_configured_logger("mi_app_name")

@ev.handler_intent(intent='intent-name')
def foo(event):
    # TODO: Implement logic required
    return event.delegate_response() # optional
...
...

def lambda_handler(event, context):
    logger.debug('Request:\n {}'.format(event))
    action = ev.execute(event)
    logger.debug('Response:\n {}'.format(action))
    return action
```

**Compile or download [precompiled file](dist):** 
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

