import logging
import re
from shockfish.events import ResponsePatching
from shockfish.constants import _path

logger = logging.getLogger(__name__)

class ResponseProtector:

    _type = "output"
    _name = "HTTP headers protector"
    _injected_script = b"<head>\n<script src=\"" + _path + b"shockfish.js\"></script>"
    _priority = 1
    
    def __init__(self, request, options=None):
        self.request = request
        self.options = options

    def run(self):

        if self.options.get("js"):
            self.request.bodyData = re.sub(b"(?i)<head>", ResponseProtector._injected_script, self.request.bodyData)

        headers = self.request.responseHeaders

        if self.options.get("secure_headers"):
            if not headers.hasHeader("X-Frame-Options"):
                self.request.setHeader("X-Frame-Options", "SAMEORIGIN")
                msg = "Added X-Frame-Options"
                ResponsePatching(__name__, msg)

            if not headers.hasHeader("X-XSS-Protection"):
                self.request.setHeader("X-XSS-Protection", "1")
                msg = "X-XSS-Protection"
                ResponsePatching(__name__, msg)

                logger.debug("Added X-XSS-Protection")
            
            if not headers.hasHeader("X-Content-Type-Options"):
                self.request.setHeader("X-Content-Type-Options", "nosniff")
                msg = "Added X-Content-Type-Options"
                ResponsePatching(__name__, msg)

        

