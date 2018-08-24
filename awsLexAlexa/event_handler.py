import logging

from .events.alexaEvent import AlexaEvent
from .events.lexEvent import LexEvent


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s:%(levelname)s: %(message)s',
#                     datefmt='%d/%m/%y %H:%M:%S')
# logger = logging.getLogger("awsLexAlexa")


def get_logger():
    logger = logging.getLogger("awsLexAlexa.handler")
    syslog = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(levelname)s: %(message)s', "%d/%m/%y %H:%M:%S")
    syslog.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(syslog)


logger = get_logger()

LEX = 'lex'
ALEXA = 'alexa'
LOGS_ATTRIBUTE = "PublishLogs"
DEFAULT_INTENT = "default"


class EventHandler:

    def __init__(self):  # Event is just a dictionary.
        self.handler_intent = {}
        self.event = None
        self.bot_platform = None  # Can be 'lex' or 'alexa'

    def register_intent(self, intent: str):
        """
        This is the decorator function to register the functions destined to validate slots
        :param intent: The name of intent to validate
        """
        intent = intent.replace(u"\u200b", "")  # To prevent copy&paste

        def wrapper(function):
            if intent not in self.handler_intent:
                self.handler_intent[intent] = function
                logger.debug("Registered handler for {}".format(intent))
            else:
                # raise KeyError('It already exists a function for intent {}'.format(intent))
                logger.error('It already exists a function for intent {}'.format(intent))
            return function

        return wrapper

    def default_intent(self):
        def wrapper(function):
            self.handler_intent[DEFAULT_INTENT] = function

        return wrapper

    @staticmethod
    def set_log_level(log_level):
        logger.setLevel(log_level)

    @staticmethod
    def detect_bot_platform(event):
        bot_platform = None
        try:
            # Check for alexa source
            assert event['request']['type']
            bot_platform = ALEXA
            logger.debug('Alexa detected')
        except KeyError:
            # Then is lex source
            bot_platform = LEX
            logger.debug('Lex detected')
        return bot_platform

    def execute(self, event: dict = None):
        # First detect the bot platform source like Lex or Alexa
        if event:
            self.bot_platform = self.detect_bot_platform(event)
            if self.bot_platform == ALEXA:
                self.event = AlexaEvent(event)
            elif self.bot_platform == LEX:
                self.event = LexEvent(event)
            else:
                raise KeyError('BotPlatform can not be detected')
        else:
            raise ValueError('"Event" need to be specificated')

        # Check if there are any sessionAttribute with "PublishLogs" key
        if self.event.get_sessionAttributes([LOGS_ATTRIBUTE]):
            logger.setLevel(logging.DEBUG)

        # Execute intent logic
        intent_name = self.event.intentName
        if intent_name in self.handler_intent:
            response = self.handler_intent[intent_name](self.event)

        # Check if default handler exists
        elif DEFAULT_INTENT in self.handler_intent:
            response = self.handler_intent[DEFAULT_INTENT](self.event)

        else:
            logger.error(self.handler_intent)
            raise NotImplementedError('There are not function for {} intent'.format(intent_name))

        return response
