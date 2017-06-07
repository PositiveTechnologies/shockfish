import re
import logging
from shockfish.events import Attack

logger = logging.getLogger(__name__)

class CRLFProtector:

    _type = "input"
    _name = "CRLF injection protector"
    _priority = 1

    def __init__(self, request, options=None):
        self.request = request
        self.options = options

    def run(self):
        crlf_regex = b".*\n.*"
        for feature in self.request.requestData:
            value = feature.get("value")
            name = feature.get("name")
            type_ = feature.get("type")
            logger.debug("Tested  type: %s, key: %s value: %s", type_, name, value)
            if re.search(crlf_regex, value):
                msg = "CRLF injection detected: {0}={1}".format(name, value)
                Attack(__name__, msg)
