import logging

from awsLexAlexa.events.eventInterface import _EventInterface

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s:%(levelname)s: %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')
logger = logging.getLogger(__name__)


class AlexaEvent(_EventInterface):
    def __init__(self, event):
        super().__init__()
        self.event = event
        self.alexa_help_mgs = None

        self.bot_platform = super().LEX
        self.sessionAttributes = self._extract_value(['session', 'attributes'])
        self.confirmationStatus = self._extract_value(['request', 'intent', 'confirmationStatus'])
        self.intentName = self._extract_value(['request', 'intent', 'name'])
        self.slots = self._extract_value(['request', 'intent', 'slots'])
