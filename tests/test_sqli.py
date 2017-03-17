from context import SQLiProtector, AttackException
from nose.tools import *

class Request():
    def __init__(self, path, data):
        self.requestData = data
        self.path = path

@raises(AttackException)
def test_sqli():
    request = Request(b"/", [{"name": b"a", "value": b"'or'1'='1"}])
    protector = SQLiProtector(request)
    protector.run()

def test_normal_data():
    request = Request(b"/", [{"name": b"a", "value": b"1"}])
    protector = SQLiProtector(request)
    try:
        protector.run()
    except:
        assert True == False
