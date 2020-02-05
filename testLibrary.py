import logging
from awsLexAlexa import
from awsLexAlexa.event_handler import *

ev = EventHandler()
logger = ev.get_configured_logger("app")
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

JSON_TEST = {'messageVersion': '1.0',
             'invocationSource': 'FulfillmentCodeHook',
             'userId': 'efxg4jifi1vy40ddxv8j52sw779p9nrc',
             'sessionAttributes': {},
             'requestAttributes': None,
             'bot': {'name': 'DavidMartinez', 'alias': '$LATEST', 'version': '$LATEST'},
             'outputDialogMode': 'Text',
             'currentIntent': {
                 'name': 'test',
                 'slots': {'Uniforms': 'now'},
                 'slotDetails': {'Uniforms': {'resolutions': [{'value': 'now'}], 'originalValue': 'now'}},
                 'confirmationStatus': 'None'
             },
             'inputTranscript': 'now'}


@ev.default_intent()
def default(event):

    logger.info(event.event)
    return event.close_response("close response")


# @ev.register_intent(intent='newEvents')


def lambda_handler(event, context):
    logger.debug('Request:\n {}'.format(event))
    action = ev.execute(event)
    logger.debug('Response:\n {}'.format(action))
    return action


if __name__ == '__main__':
    lambda_handler(JSON_TEST, None)
    # logger = logging.getLogger("aws")
    # print(logger.name.split('.')[0])
