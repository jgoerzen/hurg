from GopherComm import GopherComm
from UserList import UserList
from UserDict import UserDict
import urllib
import cgi

class GopherFile(UserDict):
    def makefromstring(self, host, port, string):
        self.data = {}
        string = string.strip()

        parts = string.split("\t")
        
        self.data['type'] = parts[0][0]
        self.data['username'] = parts[0][1:]
        self.data['selector'] = parts[1]
        self.data['host'] = parts[2]
        self.data['port'] = parts[3]

        if self.data['host'] == '+':
            self.data['host'] = host

        if self.data['port'] == '+':
            self.data['port'] = port

    def gettype(self):
        return self.data['type']

    def getusername(self):
        return self.data['username']

    def getselector(self):
        return self.data['selector']

    def gethost(self):
        return self.data['host']

    def getport(self):
        return self.data['port']

    def getHTMLdirline(self, baseURL="/g2html"):
        return '<A HREF="%s">%s</A>' % \
               ((baseURL + '?' + urllib.urlencode(self.data)),
                cgi.escape(self.getusername()))

class GopherDir(UserList):
    def __init__(self, foo=[]):
        self.data = foo
    
    def get(self, host, port=70, selector=""):
        gc = GopherComm()
        sock = gc.getdocsocket(host, port, selector).makefile()
        self.data = []

        while 1:
            line = sock.readline()
            if not line: break
            line = line.strip()

            if line == '.': break

            if not line[0] == '+':
                gf = GopherFile()
                gf.makefromstring(host, port, line)
                self.data.append(gf)
            
