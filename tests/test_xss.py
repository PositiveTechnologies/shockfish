from context import XSSProtector, AttackException
from nose.tools import *

class Request():
    def __init__(self, path, data):
        self.requestData = data
        self.path = path

@raises(AttackException)
def test_xss():
    request = Request(b"/", [{"name": b"a", "value": b"<script>alert(1)</script>"}])
    protector = XSSProtector(request)
    protector.run()

def test_normal_data():
    request = Request(b"/", [{"name": b"a", "value": b"1"}])
    protector = XSSProtector(request)
    try:
        protector.run()
    except:
        assert True == False
