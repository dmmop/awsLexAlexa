import logging

from .events.alexaEvent import AlexaEvent
from .events.lexEvent import LexEvent
from .logs.configLogs import get_configured_logger, assign_userId_filter

get_configured_logger("awsLexAlexa")

logger = logging.getLogger("awsLexAlexa.handler")

LEX = 'lex'
ALEXA = 'alexa'
DEFAULT_INTENT = "default"

__all__ = ["EventHandler", "LEX", "ALEXA"]


class EventHandler:

    def __init__(self):  # Event is just a dictionary.
        self.handler_intent = {}
        self.event = None
        self.loggers = [logger]

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

    def get_configured_logger(self, parent):
        """
        Provide a logger preconfigured like library to facilitate homogeneous logs.
        :param parent: Parent of the new logger
        :return: logger configured
        """
        user_logger = get_configured_logger(parent)
        self.loggers.append(user_logger)
        return user_logger

    @staticmethod
    def set_log_level(log_level):
        """
        Modify the level of logs in library.
        :param log_level: New level to set.
        """
        logging.getLogger("awsLexAlexa").setLevel(log_level)

    @staticmethod
    def _detect_bot_platform(event):
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
            bot_platform = self._detect_bot_platform(event)
            if bot_platform == ALEXA:
                self.event = AlexaEvent(event)
            elif bot_platform == LEX:
                self.event = LexEvent(event)
            else:
                raise KeyError('BotPlatform can not be detected')
        else:
            raise ValueError('"Event" need to be specificated')

        # Add userID to log trace
        if self.event.userId:
            # [assign_userId_filter(x.name.split('.')[0], self.event.userId) for x in self.loggers]
            for x in self.loggers:
                assign_userId_filter(x.name.split('.')[0], self.event.userId)

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
