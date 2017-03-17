import logging

logger = logging.getLogger(__name__)


class Attack:
    def __init__(self, protector, message):
        logger.critical(protector + ": " + message)
        raise AttackException


class RequestPatching(Exception):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ResponsePatching:
    def __init__(self, protector, message):
        logger.info(protector + ": " + message)


class AttackException(Exception):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ResponseSpoofing(Exception):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
