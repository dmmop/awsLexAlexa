import logging


class UserIdFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """

    def __init__(self):
        super().__init__()
        self.userId = "UnknownId"

    def filter(self, record):
        record.userId = self.userId
        return True


def get_configured_logger(parent):
    logger = logging.getLogger(parent)
    logger.propagate = False  # duplicated messages in cloudwatch
    formatter = logging.Formatter('[%(asctime)-17s] [%(levelname)-7s] [%(name)-21s] %(userId)-32s - %(message)s',
                                  "%d/%m/%y %H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(UserIdFilter())

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def assign_userId_filter(parent, userId):
    for handler in logging.getLogger(parent).handlers:
        for filter in handler.filters:
            if isinstance(filter, UserIdFilter):
                filter.userId = userId
