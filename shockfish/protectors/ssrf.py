import re
import logging
from shockfish.events import Attack

logger = logging.getLogger(__name__)

class SSRFProtector:

    _type = "input"
    _name = "SSRF protector"
    _priority = 1
    
    def __init__(self, request, options=None):
        self.request = request
        self.options = options

    def run(self):
        """ 
        SSRF detection.
        """
        """
        The folowing regex is vulnerable to "Syntax bypass".
        """
        ssrf_regex = b"(gopher|jar|tftp|php|phar|ldap|dict|ssh2|file|imap|pop3|smtp|telnet|mailto|data|http|https):\/\/"

        """
        The following regex is vulnerable to "Logical bypass".
        For example, you can use the following IP-addresses:
        - ::1
        - ::
        - 425.510.425.510
        - 2852039166

        Source: http://www.agarri.fr/docs/AppSecEU15-Server_side_browsing_considered_harmful.pdf
        """
        ip_regex = b"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        for feature in self.request.requestData:
            if feature.get("type") == "request_header":
                continue
            value = feature.get("value")
            name = feature.get("name")
            type_ = feature.get("type")
            logger.debug("Tested  type: %s, key: %s value: %s", type_, name, value)
            if re.search(ssrf_regex, value) or re.search(ip_regex, value):
                msg = "SSRF attack detected: {0}={1}".format(name, value)
                Attack(__name__, msg)
