from GopherComm import GopherComm
from UserList import UserList
from UserDict import UserDict
import urllib
import cgi
import types
import sys

class GopherFile:
    implementsTypes = []
    def __init__(self):
        self.entrydata = {}

    def makefromstring(self, host, port, string):
        self.entrydata = {}
        string = string.strip()

        parts = string.split("\t")
        
        self.settype(parts[0][0])
        self.setusername(parts[0][1:])
        self.setselector(parts[1])
        self.sethost(parts[2])
        self.setport(parts[3])

        if self.gethost() == '+':
            self.sethost(host)

        if self.getport() == '+':
            self.setport(port)

        self.rebless()

    def settype(self, type):
        self.entrydata['type'] = type

    def setusername(self, username):
        self.entrydata['username'] = username

    def setselector(self, selector):
        self.entrydata['selector'] = selector

    def sethost(self, host):
        self.entrydata['host'] = host

    def setport(self, port):
        self.entrydata['port'] = port

    def gettype(self):
        return self.entrydata['type']

    def getusername(self):
        return self.entrydata['username']

    def getselector(self):
        return self.entrydata['selector']

    def gethost(self):
        return self.entrydata['host']

    def getport(self):
        return self.entrydata['port']

    def getHTMLusername(self):
        return cgi.escape(self.getusername())

    def getHTMLlink(self, baseURL="/g2html"):
        return baseURL + '?' +urllib.urlencode(self.entrydata)

    def getHTMLdirline(self, baseURL="/g2html/g2html"):
        return '<A HREF="%s">%s</A>' % (self.getHTMLlink(baseURL),
                                        self.getHTMLusername())

    def rebless(self):
        for mod in globals().keys():
            val = globals()[mod]
            if not type(val) is types.ClassType: continue
            if not issubclass(val, GopherFile): continue
            if (self.gettype() in val.implementsTypes):
                self.__class__ = val
                self.blessinit()
                return self
        return self

    def blessinit(self):
        pass

    def display(self):
        print "Content-Type: text/plain"
        print
        gc = GopherComm()
        sock = gc.getdocsocket(self.gethost(), self.getport(),
                               self.getselector()).makefile()
        copy(sock, sys.stdout)

class GopherFileInfo(GopherFile):
    implementsTypes = ['i']
    
    def getHTMLdirline(self):
        return "<TT>" + self.getusername() + "</TT>"

class GopherFileDir(GopherFile, UserList):
    implementsTypes = ['1']
    
    def __init__(self, foo=[]):
        self.data = foo
        GopherFile.__init__(self)

    def blessinit(self):
        self.data = []
    
    def getfromnet(self):
        gc = GopherComm()
        sock = gc.getdocsocket(self.gethost(), self.getport(),
                               self.getselector()).makefile()
        self.data = []

        while 1:
            line = sock.readline()
            if not line: break
            line = line.strip()

            if line == '.': break

            if not line[0] == '+':
                gf = GopherFile()
                gf.makefromstring(self.gethost(), self.getport(), line)
                gf.rebless()
                self.data.append(gf)
    
    def display(self):
        self.getfromnet()
        print "Content-Type: text/html"
        print
        print "<HTML><BODY>"
        for entry in self.data:
            print entry.getHTMLdirline() + "<BR>"
        print "</BODY></HTML>"


def copy(infile, outfile):
    while 1:
        line = infile.read(4096)
        if len(line) == 0: break
        outfile.write(line)
