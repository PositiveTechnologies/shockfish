#!/usr/bin/env python
"""
Core module implementing processing of HTTP requests.
"""
import json
import sys
import logging
import os

from twisted.internet import reactor, protocol
from twisted.web import proxy, http

from shockfish.engine  import EngineFactory
from shockfish.events  import *
from shockfish.utils import extractFeatures, getFileContent, Locator, mergeArgs

logger = logging.getLogger("core")
config = Locator.get("Config")

class ProxyClient(http.HTTPClient):
    """
    The proxy client connects to the real server, fetches the resource and
    sends it back to the original client.
    """
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        self.contentLength = None
        self.originalRequest.probably_raw_xml = False
    
    def sendRequestLine(self):
        """
        Send request line.
        Request-line: Method SP Request-URI SP HTTP-Version CRLF.
        """
        self.sendCommand(self.method, self.uri)

    def sendHeaders(self):
        """
        Send HTTP headers.
        """
        for key, values in self.headers:
            for value in values:
                if key == b"Connection":
                    value = b"close"
                self.sendHeader(key, value)
        self.endHeaders()

    def sendPostData(self):
        """
        Send POST data.
        """
        self.transport.write(self.postData)
    
    def connectionMade(self):
        """
        On new connection sends HTTP packet to protected web server.
        """
        self.sendRequestLine()
        self.sendHeaders()
        if self.method == b"POST":
            self.sendPostData()

    def handleHeader(self, key, value):
        """
        Called every time a header is received.
        """
        if key.lower() == b"content-length":
            self.contentLength = value
        else:
            self.originalRequest.responseHeaders.addRawHeader(key, value)

    def sendForbiddenMessage(self):
        """
        Send forbidden message.
        """
        logger.debug("Send forbidden message")
        self.originalRequest.setResponseCode(403)
        self.originalRequest.setHeader("Server", "shockfish")
        self.originalRequest.responseHeaders.removeHeader("Content-Type")
        self.originalRequest.responseHeaders.removeHeader("Date")
        self.originalRequest.finish()
        self.transport.loseConnection()

    def handleResponse(self, data):
        """
        Undocumented method.
        Runs output analyzer on HTTP response, returns 403 on attack.
        """
        self.originalRequest.bodyData = data
        output_engine = Locator.get("OutputEngine")
        try:
            output_engine.process(self.originalRequest)
        except AttackException as e:
            self.sendForbiddenMessage()
            return
        self.originalRequest.write(self.originalRequest.bodyData)
        self.originalRequest.finish()
        self.transport.loseConnection()
    
    
class ProxyClientFactory(protocol.ClientFactory):
    """
    Factory for ProxyRequest.
    """
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.protocol = ProxyClient
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        self.originalRequest.bodyData = None
    
    def buildProtocol(self, addr):
        return self.protocol(self.method, self.uri, self.postData,
                             self.headers, self.originalRequest)
    
    def clientConnectionFailed(self, connector, reason):
        self.originalRequest.setResponseCode(504)
        self.originalRequest.finish()
        self.transport.loseConnection()


class ProxyRequest(http.Request):
    """
    Request object implementing arguments parsing and normalization, request routing and analysis
    """
    def __init__(self, channel, queued, reactor=reactor):
        http.Request.__init__(self, channel, queued)
        self.reactor = reactor
        self.request_data = []
    
    def sendForbiddenMessage(self):
        """
        Send forbidden message.
        """
        logger.debug("Send forbidden message")
        self.setResponseCode(403)
        self.setHeader("Connection", "close")
        self.setHeader("Server", "shockfish")
        self.finish()
        self.transport.loseConnection()

    def process(self):
        """
        Processes request.
        """
        body = self.content.read()
        
        post_args = http.parse_qs(body)
        mergeArgs(self.args, post_args)

        input_engine = Locator.get("InputEngine")

        
        self.requestData = extractFeatures(self, config)
        
        try:
            input_engine.process(self)
        except ResponseSpoofing as e:
            return
        except AttackException as e:
            self.sendForbiddenMessage()
            return

        port = config.backend.get("port")
        host = config.backend.get("host")

        
        factory = ProxyClientFactory(self.method, self.uri, body,
                                 self.requestHeaders.getAllRawHeaders(),
                                 self)
        
        self.reactor.connectTCP(host, port, factory)
        

class TransparentProxy(http.HTTPChannel):
    requestFactory = ProxyRequest


class ProxyFactory(http.HTTPFactory):
    protocol = TransparentProxy


def runProxy():

    inputEngine = EngineFactory.buildEngine(["input"], config)
    outputEngine = EngineFactory.buildEngine(["output"], config)

    Locator.load("InputEngine", inputEngine)
    Locator.load("OutputEngine", outputEngine)

    factory = ProxyFactory()

    interface = config.virtualServer.get("interface")
    port = config.virtualServer.get("port")
    try:
        reactor.listenTCP(port, factory, interface=interface)
    except Exception as err:
        print(err)
        logger.error(err)
        sys.exit(1)
    else:
        print("Shockfish core has been started at %s : %s." %(interface, port))
        logger.debug("Shockfish core has been started at %s : %s." %(interface, port))
    
    reactor.run()
    sys.exit(0)

if __name__ == "__main__":
    runProxy()
