import logging

from awsLexAlexa.events.lexEvent import LexEvent

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s:%(levelname)s: %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')
logger = logging.getLogger(__name__)


class LexResponse(LexEvent):
    def delegate_response(self):
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

    @staticmethod
    def elicit_intent_response(msg,
                               reprompt_msg=None,
                               msg_type='PlainText',
                               reprompt_type='PlainText'):
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

    @staticmethod
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
