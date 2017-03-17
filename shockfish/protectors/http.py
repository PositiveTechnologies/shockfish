import re
import logging
from shockfish.events import Attack

logger = logging.getLogger(__name__)

class HTTPProtector:

    _type = "input"
    _name = "HTTP protector"
    _priority = 1
    
    def __init__(self, request, options=None):
        self.request = request
        self.options = options

    def run(self):
        allowed_methods = self.options.get("allowed_methods")
        if not self.request.method.decode("ascii") in allowed_methods:
            msg = "HTTP method is not allowed: {0}".format(self.request.method)
            Attack(__name__, msg)

