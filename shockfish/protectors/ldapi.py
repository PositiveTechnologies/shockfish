import re
import logging
from shockfish.events import Attack

logger = logging.getLogger(__name__)

class LDAPiProtector:

    _type = "input"
    _name = "LDAP injection protector"
    _priority = 1

    def __init__(self, request, options=None):
        self.request = request
        self.options = options

    def run(self):
        """
        The folowing regex is vulnerable to "Syntax bypass": spaces are ignored by parsers.
        """
        ldap_regex = b"^[^:\(\)\&\|\!\<\>\~]*\)(?:\((?:[^,\(\)\=\&\|\!\<\>\~]+[><~]?=|[&!|](?:\)|\()?)|\)\([\&\|\!]|[&!|]\([^\(\)\=\&\|\!\<\>\~]+[><~]?=[^:\(\)\&\|\!\<\>\~]*|(?:\))+%00)"
        for feature in self.request.requestData:
            value = feature.get("value")
            name = feature.get("name")
            type_ = feature.get("type")
            logger.debug("Tested  type: %s, key: %s value: %s", type_, name, value)
            if re.search(ldap_regex, value, flags=re.IGNORECASE ):
                msg = "LDAP injection detected: {0}={1}".format(name, value)
                Attack(__name__, msg)
