from socket import *

class GopherComm:
    def __init__(self):
        self.VERSION = '$Id: GopherComm.py,v 1.4 2001/08/28 20:06:15 jgoerzen Exp $'
    
    def getdocsocket(self, host, port=70, selector=""):
        socket = self.connectTCP(host, port)
        socket.send(selector + "\r\n")
        return socket

    def connectTCP(self, host, port):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        return s
