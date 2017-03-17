import re
import logging
from shockfish.events import Attack

logger = logging.getLogger(__name__)

class XSSProtector:

    _type = "input"
    _name = "XSS protector"
    _priority = 1

    def __init__(self, request, options=None):
            self.request = request
            self.options = options

    def isxss(self, payload):
        """
        The folowing regexes are from RisingStack protect module:
        https://github.com/RisingStack/protect/blob/master/lib/rules/xss.js.
        """
        xss = b"((%3C)|<)((%2F)|/)*[a-z0-9%]+((%3E)|>)"
        imgSrcXss = b"((%3C)|<)((%69)|i|(%49))((%6D)|m|(%4D))((%67)|g|(%47))[^\n]+((%3E)|>)"
        return re.search(xss, payload, flags=re.IGNORECASE ) or re.search(imgSrcXss, payload, flags=re.IGNORECASE)

    def run(self):
        for feature in self.request.requestData:
            value = feature.get("value")
            name = feature.get("name")
            type_ = feature.get("type")
            logger.debug("Tested  type: %s, key: %s value: %s", type_, name, value)
            if self.isxss(value):
                msg = "XSS detected: {0}={1}".format(name, value)
                Attack(__name__, msg)
