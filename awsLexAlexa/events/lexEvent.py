import logging

from awsLexAlexa.events.eventInterface import _EventInterface

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s:%(levelname)s: %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')
logger = logging.getLogger(__name__)


class LexEvent(_EventInterface):
    class _Bot:
        def __init__(self, event):
            self.name = event._extract_value(['bot', 'name'])
            self.alias = event._extract_value(['bot', 'alias'])
            self.version = event._extract_value(['bot', 'version'])

    def __init__(self, event):  # Event is just a dictionary.

        super().__init__()
        self.event = event

        self.bot_platform = super().LEX
        self.messageVersion = self._extract_value(['messageVersion'])
        self.invocationSource = self._extract_value(['invocationSource'])
        self.userId = self._extract_value(['userId'])
        self.sessionAttributes = self._extract_value(['sessionAttributes'])
        self.requestAttributes = self._extract_value(['requestAttributes'])
        self.bot = self._Bot(self)
        self.outputDialogMode = self._extract_value(['outputDialogMode'])
        self.confirmationStatus = self._extract_value(['currentIntent', 'confirmationStatus'])
        self.inputTranscript = self._extract_value(['inputTranscript'])
        self.intentName = self._extract_value(['currentIntent', 'name'])
        self.slots = self._extract_value(['currentIntent', 'slots'])
