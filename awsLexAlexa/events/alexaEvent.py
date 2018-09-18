import json
import logging

from awsLexAlexa.events.eventInterface import _EventInterface

logger = logging.getLogger("awsLexAlexa.alexa")


class AlexaEvent(_EventInterface):
    def __init__(self, event):
        super().__init__()
        self.event = event
        self.alexa_help_mgs = None

        self.bot_platform = super().LEX
        self.confirmationStatus = self._extract_value(['request', 'intent', 'confirmationStatus'])
        self.intentName = self._extract_value(['request', 'intent', 'name'])
        # self.sessionAttributes = self._extract_value(['session', 'attributes'])
        # self.slots = self._extract_value(['request', 'intent', 'slots'])
        self.slots = self.Slots()
        if self._extract_value(['request', 'intent', 'slots']):
            for key, value in self._extract_value(['request', 'intent', 'slots']).items():
                self.slots.__setattr__(key, value)

        self.sessionAttributes = self.SessionAttributes()
        if self._extract_value(['session', 'attributes']):
            for key, value in self._extract_value(['session', 'attributes']):
                self.slots.__setattr__(key, value)

    def delegate_response(self):
        """
        This response delegates Alexa to choose the next course of action based on the bot
        configuration.
        :param slots_dict: Dictionary containing slot names as keys and Alexa-formatted slots as
        values. If the value for a slot is unknown, it should be set as python's None (equivalent to
        json's null).
        :param intent_name: Name of the intent to be confirmed.
        :param session_att: In case session attributes should be set, they would be fed as a
        dictionary to this parameter.
        :return: A json-formatted response that agrees with Alexa's conversational model.
        """

        directive = {"type": "Dialog.Delegate",
                     "updatedIntent": {
                         "name": self.intentName,
                         "confirmationStatus": "NONE",
                         "slots": self.slots.__dict__
                     }
                     }

        action = {
            'version': '1.0',
            'sessionAttributes': self.sessionAttributes.__dict__,
            'response': {'directives': [directive]}
        }
        logger.info('Delegate response ->\r{}'.format(json.dumps(action)))
        return action

    def elicit_slot_response(self, elicit_slot, msg,
                             reprompt_msg,
                             msg_type='PlainText',
                             reprompt_type='PlainText'):
        """
        This response informs Alexa that the user is expected to provide a slot value in the response.
        :param msg: Message to be said to the user. It should be a string containing either plain
        text or SSML text, depending on the value of 'msg_type'.
        :param reprompt_msg: Message to be said to the user after 'msg' is said and a particular
        time lapse passes. It should be a string containing either plain text or SSML text, depending
        on the value of 'reprompt_type'.
        :param intent_name: Name of the intent whose slot is to be set.
        :param elicit_slot: Name of the slot whose value is asked for.
        :param slots_dict: Dictionary containing slot names as keys and Alexa-formatted slots as
        values. If the value for a slot is unknown, it should be set as python's None (equivalent to
        json's null). Every slot that should be set by the user (maybe after an unsuccessful
        validation), should be set to None as well.
        :param msg_type: It indicates the output voice format. Its value should be either 'PlainText'
        or 'SSML'.
        :param reprompt_type: It indicates the output voice format for 'reprompt_msg'. Its value
        should be either 'PlainText' or 'SSML'.
        :param session_att: In case session attributes should be set, they would be fed as a
        dictionary to this parameter.
        :return: A json-formatted response that agrees with Alexa's conversational model.
        """
        self.set_slot(key_name=elicit_slot)

        directive = {
            "type": "Dialog.ElicitSlot",
            "slotToElicit": elicit_slot,
            "updatedIntent": {
                "name": self.intentName,
                "confirmationStatus": "NONE",
                "slots": self.slots.__dict__
            }
        }

        action = self.build_response(msg=msg,
                                     msg_type=msg_type,
                                     reprompt_msg=reprompt_msg,
                                     reprompt_type=reprompt_type,
                                     directives=[directive])
        logger.info('ElicitSlot response ->\r{}'.format(json.dumps(action)))
        return action

    def elicit_intent_response(self, msg, reprompt_msg,
                               msg_type='PlainText',
                               reprompt_type='PlainText'):
        """
        This response informs Alexa that the user is expected to respond with an utterance that
        includes an intent.
        :param msg: Message to be said to the user. It should be a string containing either plain
        text or SSML text, depending on the value of 'msg_type'.
        :param reprompt_msg: Message to be said to the user after 'msg' is said and a particular
        time lapse passes. It should be a string containing either plain text or SSML text, depending
        on the value of 'reprompt_type'.
        :param msg_type: It indicates the output voice format. Its value should be either 'PlainText'
        or 'SSML'.
        :param reprompt_type: It indicates the output voice format for 'reprompt_msg'. Its value
        should be either 'PlainText' or 'SSML'.
        :param session_att: In case session attributes should be set, they would be fed as a
        dictionary to this parameter.
        :return: A json-formatted response that agrees with Alexa's conversational model.
        """

        action = self.build_response(msg=msg,
                                     msg_type=msg_type,
                                     reprompt_msg=reprompt_msg,
                                     reprompt_type=reprompt_type)
        logger.info('ElicitIntent response ->\r{}'.format(json.dumps(action)))
        return action

    def confirm_intent_response(self, msg, reprompt_msg,
                                msg_type='PlainText',
                                reprompt_type='PlainText'):
        """
        This response informs Alexa that the user is expected to give a yes or no answer to confirm
        or deny the current intent.
        :param msg: Message to be said to the user. It should be a string containing either plain
        text or SSML text, depending on the value of 'msg_type'.
        :param reprompt_msg: Message to be said to the user after 'msg' is said and a particular
        time lapse passes. It should be a string containing either plain text or SSML text, depending
        on the value of 'reprompt_type'.
        :param intent_name: Name of the intent to be confirmed.
        :param slots_dict: Dictionary containing slot names as keys and Alexa-formatted slots as
        values. If the value for a slot is unknown, it should be set as python's None (equivalent to
        json's null).
        :param msg_type: It indicates the output voice format. Its value should be either 'PlainText'
        or 'SSML'.
        :param reprompt_type: It indicates the output voice format for 'reprompt_msg'. Its value
        should be either 'PlainText' or 'SSML'.
        :param session_att: In case session attributes should be set, they would be fed as a
        dictionary to this parameter.
        :return: A json-formatted response that agrees with Alexa's conversational model.
        """

        directive = {
            "type": "Dialog.ConfirmIntent",
            "updatedIntent": {
                "name": self.intentName,
                "confirmationStatus": "NONE",
                "slots": self.slots.__dict__
            }
        }

        action = self.build_response(msg=msg,
                                     msg_type=msg_type,
                                     reprompt_msg=reprompt_msg,
                                     reprompt_type=reprompt_type,
                                     directives=[directive])
        logger.info('ConfirmIntent response ->\r{}'.format(json.dumps(action)))
        return action

    def close_response(self, msg,
                       reprompt_msg='What else can I do for you?',
                       msg_type='PlainText',
                       reprompt_type='PlainText'):
        """
        This response tells alexa not to expect a further response from the user within the current
        intent. However, Alexa will be ready to answer further questions since the session will not
        be directly closed after this response. It is used generally when every action related to an
        intent has been done.
        :param msg: Message to be said to the user. It should be a string containing either plain
        text or SSML text, depending on the value of 'msg_type'.
        :param reprompt_msg: Message to be said to the user after 'msg' is said and a particular
        time lapse passes. It should be a string containing either plain text or SSML text, depending
        on the value of 'reprompt_type'.
        :param msg_type: It indicates the output voice format for 'msg'. Its value should be either
        'PlainText' or 'SSML'.
        :param reprompt_type: It indicates the output voice format for 'reprompt_msg'. Its value
        should be either 'PlainText' or 'SSML'.
        :param session_att: In case session attributes should be set, they would be fed as a
        dictionary to this parameter.
        :return: A json-formatted response that agrees with Alexa's conversational model.
        """

        action = self.build_response(msg=msg,
                                     msg_type=msg_type,
                                     reprompt_msg=reprompt_msg,
                                     reprompt_type=reprompt_type,
                                     should_end_session=False)
        logger.info('Close response ->\r{}'.format(json.dumps(action)))
        return action

    def end_response(self, msg, msg_type='PlainText'):
        """
        This response, which is not included in dialogs_lex.py, should be used to finish Alexa's
        Skill's session.
        :param msg: Message to be said to the user. It should be a string containing either plain
        text or SSML text, depending on the value of 'msg_type'.
        :param msg_type: It indicates the output voice format for 'msg'. Its value should be either
        'PlainText' or 'SSML'.
        :param session_att: In case session attributes should be set, they would be fed as a
        dictionary to this parameter.
        :return: A json-formatted response that agrees with Alexa's conversational model.
        """

        action = self.build_response(msg=msg,
                                     msg_type=msg_type,
                                     should_end_session=True)

        logger.info('End response ->\r{}'.format(json.dumps(action)))
        return action

    def build_response(self, msg="",
                       msg_type='PlainText',
                       reprompt_msg="",
                       reprompt_type='PlainText',
                       directives=None,
                       should_end_session=False):
        """
        This is the generic template to create a response for Alexa.
        :param intent_name: Name of the current intent.
        :param msg: Message to be said to the user. It should be a string containing either plain
        text or SSML text, depending on the value of 'msg_type'.
        :param msg_type: It indicates the output voice format. Its value should be either 'PlainText'
        or 'SSML'.
        :param reprompt_msg: Message to be said to the user after 'msg' is said and a particular
        time lapse passes. It should be a string containing either plain text or SSML text, depending
        on the value of 'reprompt_type'.
        :param reprompt_type: It indicates the output voice format for 'reprompt_msg'. Its value
        should be either 'PlainText' or 'SSML'.
        :param directives: Vector containing extra directives that should be included in the
        response. For example, dialog-handling features are included here.
        :param should_end_session: True if Alexa's Skill should end after this message,
        False otherwise.
        :param session_att: In case session attributes should be set, they would be fed as a
        dictionary to this parameter.
        :return: A json-formatted response that agrees with Alexa's conversational model.
        """
        output_speech = {'type': msg_type}
        if msg_type == 'PlainText':
            output_speech['text'] = msg
        elif msg_type == 'SSML':
            output_speech['ssml'] = msg
        else:
            raise ValueError("msg_type should be either 'PlainText' or 'SSML'.")

        reprompt_output_speech = {'type': reprompt_type}
        if msg_type == 'PlainText':
            reprompt_output_speech['text'] = reprompt_msg
        elif msg_type == 'SSML':
            reprompt_output_speech['ssml'] = reprompt_msg
        else:
            raise ValueError("reprompt_type should be either 'PlainText' or 'SSML'.")

        response = {
            'outputSpeech': output_speech,
            'card': {
                'type': 'Simple',
                'title': self.intentName,
                'content': msg
            },
            'reprompt': {
                'outputSpeech': reprompt_output_speech
            },
            'directives': directives,
            'shouldEndSession': should_end_session
        }

        action = {
            'version': '1.0',
            'sessionAttributes': self.sessionAttributes.__dict__,
            'response': response
        }

        return action
