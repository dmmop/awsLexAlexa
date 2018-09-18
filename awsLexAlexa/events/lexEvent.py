import json
import logging

from awsLexAlexa.events.eventInterface import _EventInterface

logger = logging.getLogger("awsLexAlexa.lex")


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
        self.requestAttributes = self._extract_value(['requestAttributes'])
        self.bot = self._Bot(self)
        self.outputDialogMode = self._extract_value(['outputDialogMode'])
        self.confirmationStatus = self._extract_value(['currentIntent', 'confirmationStatus'])
        self.inputTranscript = self._extract_value(['inputTranscript'])
        self.intentName = self._extract_value(['currentIntent', 'name'])

        self.slots = self.Slots()
        if self._extract_value(['currentIntent', 'slots']):
            for key, value in self._extract_value(['currentIntent', 'slots']).items():
                self.slots.__setattr__(key, value)

        self.sessionAttributes = self.SessionAttributes()
        if self._extract_value(['sessionAttributes']):
            for key, value in self._extract_value(['sessionAttributes']):
                self.slots.__setattr__(key, value)

        # logger.setLevel(self.get_logger_level())

    def delegate_response(self):
        """"
        This response delegate Lex to choose the next course of action based on the configuration.
        """

        action = {
            "sessionAttributes": self.sessionAttributes.__dict__,
            "dialogAction": {
                "type": "Delegate",
                "slots": self.slots.__dict__,
            }
        }
        logger.info('Delegate response ->\r {}'.format(json.dumps(action)))
        return action

    def elicit_slot_response(self, elicit_slot, msg,
                             reprompt_msg=None,
                             msg_type='PlainText',
                             reprompt_type='PlainText'):
        """
        This response inform Lex that there are incorrect slot value, and must be fill again.
        :param elicit_slot: Slot with bad value.
        :param msg: Message to be said to the user. It should be a string containing a text or SSML text,
         depending on the value of de 'msg_type'.
        :param msg_type: It indicate the output voice format. Its value should be either 'PlainText' or 'SSML'.
        :param reprompt_msg: Slot for polymorphism with Alexa implementation.
        :param reprompt_type: Slot for polymorphism with Alexa implementation.
        :return: A json-formatted responses that agrees with Lex's API.
        """
        self.set_slot(key_name=elicit_slot)
        action = {
            "sessionAttributes": self.sessionAttributes.__dict__,
            "dialogAction": {
                "type": "ElicitSlot",
                "message": {
                    "contentType": msg_type,
                    "content": msg
                },
                "intentName": self.intentName,
                "slots": self.slots.__dict__,
                "slotToElicit": elicit_slot
            }
        }
        logger.info('ElicitSlot response ->\r {}'.format(json.dumps(action)))
        return action

    def elicit_intent_response(self, msg,
                               reprompt_msg=None,
                               msg_type='PlainText',
                               reprompt_type='PlainText'):
        """
        :param msg: Message to be said to the user. It should be a string containing a text or SSML text,
         depending on the value of de 'msg_type'.
        :param msg_type: It indicate the output voice format. Its value should be either 'PlainText' or 'SSML'.
        :param reprompt_msg: Slot for polymorphism with Alexa implementation.
        :param reprompt_type: Slot for polymorphism with Alexa implementation.
        :return: A json-formatted responses that agrees with Lex's API.
        """

        action = {
            "sessionAttributes": self.sessionAttributes.__dict__,
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": msg_type,
                    "content": msg
                }
            }
        }
        logger.info('ElicitIntent response ->\r {}'.format(json.dumps(action)))
        return action

    def confirm_intent_response(self, msg,
                                reprompt_msg=None,
                                msg_type='PlainText',
                                reprompt_type='PlainText'):
        action = {
            "sessionAttributes": self.sessionAttributes.__dict__,
            "dialogAction": {
                "type": "ConfirmIntent",
                "intentName": self.intentName,
                "slots": self.slots.__dict__,
                "message": {
                    "contentType": msg_type,
                    "content": msg
                }
            }
        }
        logger.info('ConfirmIntent response ->\r {}'.format(json.dumps(action)))
        return action

    def close_response(self, msg, msg_type='PlainText', fulfilled=True):
        fulfilled_state = 'Fulfilled' if fulfilled else 'Failed'
        action = {
            "sessionAttributes": self.sessionAttributes.__dict__,
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": fulfilled_state,
                "message": {
                    "contentType": msg_type,
                    "content": msg
                }
            }
        }
        logger.info('Close response ->\r {}'.format(json.dumps(action)))

        return action

    def end_response(self, msg, msg_type='PlainText'):
        self.close_response(msg, msg_type)
