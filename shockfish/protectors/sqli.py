import pylibinjection
import logging
from shockfish.events import Attack

logger = logging.getLogger(__name__)

class SQLiProtector:

    _type = "input"
    _name = "SQL injection protector"
    _priority = 1

    def __init__(self, request, options=None):
        self.request = request
        self.options = options

    def issqli(self, payload):
        injection = pylibinjection.detect_sqli(payload)
        return injection["sqli"]

    def run(self):
        for feature in self.request.requestData:
            value = feature.get("value")
            name = feature.get("name")
            type_ = feature.get("type")
            logger.debug("Tested  type: %s, key: %s value: %s", type_, name, value)
            if self.issqli(value):
                msg = "SQL injection detected: {0}={1}".format(name, value)
                Attack(__name__, msg)
