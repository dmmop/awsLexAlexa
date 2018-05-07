import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s:%(levelname)s: %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')
logger = logging.getLogger(__name__)


class _EventInterface:
    LEX = 'lex'
    ALEXA = 'alexa'

    def is_confirmed(self):
        status = False
        if self.confirmationStatus:
            status = self.confirmationStatus.lower() == 'confirmed'
        return status

    def is_denied(self):
        status = False
        if self.confirmationStatus:
            status = self.confirmationStatus.lower() == 'denied'
        return status

    def get_slot(self, key: str = None):
        return self._extract_value(keys=[key], dict=self.slots)

    def set_slot(self, key_name=None, key_value=None, allowed_empty=False):
        if key_name and (key_value or allowed_empty):
            self.slots[key_name] = key_value
        elif key_name is None:
            logger.error('"key_name" can not be None')
            raise ValueError('"key_name" can not be None')
        elif key_value is None and not allowed_empty:
            logger.error('"key_value" can not be None or must be "allowed_empty"')
            raise ValueError('"key_value" can not be None or must be "allowed_empty"')

    def get_sessionAttributes(self, key: list = None):
        return self._extract_value(keys=key, dict=self.sessionAttributes)

    def set_sessionAttributes(self, key_name=None, key_value=None, allowed_empty=False):
        if key_name and (key_value or allowed_empty):
            self.sessionAttributes[key_name] = key_value
        elif key_name is None:
            logger.error('"key_name" can not be None')
            raise ValueError('"key_name" can not be None')
        elif key_value is None and allowed_empty:
            logger.error('"key_value" can not be None or must be "allowed_empty"')
            raise ValueError('"key_value" can not be None or must be "allowed_empty"')

    def _extract_value(self, keys: list, dict: dict = None):
        """Return a value inside a dictionary (dict) no matter the nested level.

        **Example:**
        -------------
            dict = {
                "a": {
                    "b": {
                        "c": "C_Value"
                    }
                }
            }
            extract_value(dict=dict, keys=["a", "b", "c"]) -> "C_Value"

        **Attributes:**
        ----------------
        :param dict: Dictionary to extract value of key.
        :type dict: Dictionary
        :param keys: Key to search inside dict.
        :type keys: String separate by commas
        :return: Value extracted or None if fails.
        """

        if keys:
            keys = [slot.replace(u"\u200b", "") for slot in keys]  # Prevent copy&paste errors

        else:
            logger.error('Key value is empty')
            raise ValueError('"Keys" can not by empty')

        try:
            temp_dict = dict if dict else self.event
            for key in keys:
                temp_dict = temp_dict[key]
            return temp_dict
        except:
            logger.debug("Fail extracting: {}".format(keys))
            return None

    @staticmethod
    def update_dict_value(dictionary: dict = None, key=None, value=None):
        new_dict = dictionary.copy()
        if dictionary is None:
            logger.error('Any dictionary is required')
            raise ValueError('Any dictionary is required')
        elif key is None:
            logger.error('\"key\" can not be None')
            raise ValueError('\"key\" can not be None')
        else:
            new_dict[key] = value
        return new_dict
