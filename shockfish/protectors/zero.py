import re
import logging
from shockfish.events import ResponseSpoofing
from shockfish.constants import _path
import shockfish.utils as utils

logger = logging.getLogger(__name__)


class ZeroProtector:

    _type = "input"
    _name = "Zero protector"
    _priority = 0
    
    def __init__(self, request, options=None):
        self.request = request
        self.options = options

    def run(self):
        if self.request.path.startswith(_path):
            path = self.request.path[len(_path):]
            content = utils.getFileContent("shockfish/fixtures/www/" + path.decode())
            self.request.setHeader("Content-Type", "type/javascript")
            self.request.setHeader("Connection", "close")
            self.request.write(content)
            self.request.finish()
            raise(ResponseSpoofing)
