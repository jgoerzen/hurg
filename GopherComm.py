from socket import *

class GopherComm:
    def __init__(self):
        self.VERSION = '$Id: GopherComm.py,v 1.3 2001/08/28 19:11:46 jgoerzen Exp $'
    
    def getdocsocket(self, host, port=70, selector=""):
        socket = self.connectTCP(host, proto)
        socket.send(selector + "\r\n")
        return sock

    def connectTCP(host, port):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(host, port)
        return s
