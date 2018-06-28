import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s:%(levelname)s: %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')
logger = logging.getLogger(__name__)


class LexResponse:
    def delegate_response(self):
        """"
        This response delegate Lex to choose the next course of action based on the configuration.
        """
        logger.debug('Delegate response.')

        action = {
            "sessionAttributes": self.sessionAttributes,
            "dialogAction": {
                "type": "Delegate",
                "slots": self.slots,
            }
        }
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
        logger.debug('Elicit slot response.')
        self.set_slot(key_name=elicit_slot, allowed_empty=True)
        action = {
            "dialogAction": {
                "type": "ElicitSlot",
                "message": {
                    "contentType": msg_type,
                    "content": msg
                },
                "intentName": self.intentName,
                "slots": self.slots,
                "slotToElicit": elicit_slot
            }
        }
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
        logger.debug('Elicit Intent response.')

        action = {
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": msg_type,
                    "content": msg
                }
            }
        }
        return action

    def confirm_intent_response(self, msg,
                                reprompt_msg=None,
                                msg_type='PlainText',
                                reprompt_type='PlainText'):
        logger.debug('Confirm Intent response.')
        action = {
            "sessionAttributes": self.sessionAttributes,
            "dialogAction": {
                "type": "ConfirmIntent",
                "intentName": self.intentName,
                "slots": self.slots,
                "message": {
                    "contentType": msg_type,
                    "content": msg
                },
            }
        }
        return action

    def close_response(msg, msg_type='PlainText', fulfilled=False):
        logger.debug('Close response.')
        fulfilled_state = 'Fulfilled' if fulfilled else 'Failed'
        action = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": fulfilled_state,
                "message": {
                    "contentType": msg_type,
                    "content": msg
                }
            }
        }

        return action

    def end_response(self, msg, msg_type='PlainText'):
        self.close_response(msg, msg_type)
        # TODO: Raise or close option
        # raise NotImplementedError('End response is not available for lex.')
