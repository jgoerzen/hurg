from GopherComm import GopherComm
from UserList import UserList
from UserDict import UserDict
import urllib
import cgi
import types

class GopherFile:
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

    def getHTMLdirline(self, baseURL="/g2html"):
        return '<A HREF="%s">%s</A>' % \
               ((baseURL + '?' + urllib.urlencode(self.entrydata)),
                cgi.escape(self.getusername()))

    def implementsType(type):
        return 0

    def rebless(self):
        for mod in dir(GopherFiles):
            print "<!-- Start: %s -->\n" % mod
            if not type(getattr(GopherFiles, mod)) is types.ClassType: continue
            print "<!-- Trying: %s -->\n" % mod
            if (getattr(GopherFiles, mod).implementsType(self.gettype())):
                print "<!-- MATCH: %s -->\n" % mod
                self.__class__ = getattr(GopherFiles, mod)
                self.blessinit()
                return self
        return self

    def blessinit(self):
        pass

class GopherFileInfo(GopherFile):
    def implementsType(type):
        return type == 'i'

    def getHTMLline(self):
        return "<TT>" + self.getusername() + "</TT>"

class GopherFileDir(GopherFile, UserList):
    def __init__(self, foo=[]):
        self.data = foo
        GopherFile.__init__(self)

    def blessinit(self):
        delf.data = []
    
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
            
    def implementsType(type):
        return type == '1'
