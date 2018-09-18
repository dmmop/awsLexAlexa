import logging

logger = logging.getLogger("awsLexAlexa.interface")


class _EventInterface:
    LEX = 'lex'
    ALEXA = 'alexa'
    LOGGER_LEVEL_ATTRIBUTE = 'PublishLog'

    class Slots():
        pass

    class SessionAttributes():
        pass

    def is_confirmed(self):
        """
        Check if the event was confirmed by user
        :return: True or False
        """
        status = False
        if self.confirmationStatus:
            status = self.confirmationStatus.lower() == 'confirmed'
        return status

    def is_denied(self):
        """
        Check if the event have been rejected by user
        :return: True or False
        """
        status = False
        if self.confirmationStatus:
            status = self.confirmationStatus.lower() == 'denied'
        return status

    def get_slot(self, key: str = None, ):
        """
        Get value from slot dict and return it
        :param key: Key name of value that you want retrieve
        :return: The value if exists or None
        """
        return self.slots.__getattribute__(key)

    def set_slot(self, key_name=None, key_value=None):
        """
        Set slot value given the key name. Set None by default,
        :param key_name: Key name of the value that want to change
        :param key_value: New value for that key
        """
        if key_name:
            # self.slots[key_name] = key_value
            self.slots.__setattr__(key_name, key_value)
        else:
            logger.error('"key_name" can not be None')
            raise ValueError('"key_name" can not be None')

    def clear_slots(self):
        """
        Set all slots to None
        """
        # self.slots = self.clear_dictionary_values(self.slots)
        for attr in self.slots.__dir__():
            if not attr.startswith("_"):
                self.slots.__setattr__(attr, None)

    def get_sessionAttributes(self, key: str = None):
        """
        Get value from session attributes dict and return it
        :param key: Key name of value that you want retrieve
        :return: The value if exists or None
        """
        return self.sessionAttributes.__getattribute__(key)

    def set_sessionAttributes(self, key_name=None, key_value=None):
        """
        Set slot value given the key name. Set None by default
        :param key_name: Key name of the value that want to change
        :param key_value: New value for that key
        """
        if key_name:
            # self.sessionAttributes[key_name] = key_value
            self.sessionAttributes.__setattr__(key_name, key_value)
        else:
            logger.error('"key_name" can not be None')
            raise ValueError('"key_name" can not be None')

    def clear_sessionAttributes(self):
        """
        Set all session attributes to None
        """
        # self.sessionAttributes = self.clear_dictionary_values(self.sessionAttributes)
        for attr in self.sessionAttributes.__dir__():
            if not attr.startswith("_"):
                self.sessionAttributes.__setattr__(attr, None)

    def get_sessionAttribute_or_slot(self, key_name=None, prefer_slots=False):
        """
        Get a value searching first in session attributes and later in slot unless "prefer_slots" is activated.
        :param key_name: Key name to retrieve.
        :param prefer_slots: False default, True to prioritize slots over session attributes
        :return: The value founded or None
        """
        value_session = self.get_sessionAttributes(key_name)
        value_slot = self.get_slot(key_name)
        if prefer_slots:
            return_value = value_slot if value_slot else value_session
        else:
            return_value = value_session if value_session else value_slot

        return return_value

    def increment_counter(self, counter_name):
        """
        Search in session attributes for a counter with the "counter_name" as key, if does not exist
        add the key with value 1 and return the new value of counter.
        :param counter_name: The name of the counter saved in session attributes
        :return: The new value of that counter
        """
        counter_value = self.get_sessionAttributes(counter_name)
        counter_value = int(counter_value) + 1 if counter_value else 1
        self.set_sessionAttributes(counter_name)
        return self.get_sessionAttributes(counter_name)

    def get_counter_value(self, counter_name):
        """
        Wrapper method of "get_sessionAttributes" that return the value of some counter
        :param counter_name:  The name of the counter saved in session attributes
        :return: The value of the counter
        """
        return self.get_sessionAttributes(counter_name)

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
    def clear_dictionary_values(dictionary: dict = None, default_value=None):
        """
        Set all first level values to "default_value"
        :param dictionary:  Dictionary to clear values
        :param default_value: Value to set all keys from dict. Default None
        :return: New dictionary with all value changes.
        """
        if dictionary is None:
            logger.error('Any dictionary is required')
            raise ValueError('Any dictionary is required')
        else:
            new_dict = dictionary.fromkeys(dictionary, default_value)
        return new_dict
