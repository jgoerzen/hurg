# $Id: GopherFiles.py,v 1.19 2001/08/29 19:28:47 jgoerzen Exp $

# The file is part of HURG
# Copyright (C) 2001 John Goerzen
# jgoerzen@complete.org
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of version 2 of the GNU General Public License
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from GopherComm import GopherComm
from UserList import UserList
from UserDict import UserDict
import urllib
import cgi
import types
import sys
import re

class GopherFile:
    implementsTypes = []
    typemap = {
        '0' : 'text/plain',
        '1' : 'application/gopherdir',
        '3' : 'error/error',
        '4' : 'application/mac-binhex40',
        '5' : 'application/octet-stream',
        '9' : 'application/octet-stream',
        's' : 'audio/basic',
        'I' : 'image/jpeg',
        'g' : 'image/gif',
        'h' : 'text/html',
        'i' : ''}

    imagemap = {
        '0' : '/icons/text.gif',
        '1' : '/icons/folder.gif',
        '4' : '/icons/binhex.gif',
        '5' : '/icons/binary.gif',
        '9' : '/icons/binary.gif',
        's' : '/icons/sound1.gif',
        'I' : '/icons/image3.gif',
        'g' : '/icons/image3.gif',
        'h' : '/icons/text.gif',
        'i' : None
        }
    
    def __init__(self, host=None, port=70, type='0', selector=None,
                 username=None):
        self.entrydata = {}
        self.spiel = ''

        self.sethost(host)
        self.setport(port)
        self.settype(type)
        self.setselector(selector)
        self.setusername(username)

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
        self.entrydata['port'] = int(port)

    def setspiel(self, spiel):
        self.spiel = spiel

    def getspiel(self):
        return self.spiel

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

    def getHTMLusername(self, allowblank=1):
        if allowblank:
            return cgi.escape(self.getusername())
        else:
            if len(self.getusername()) < 1:
                return '[No title]'
            else:
                return self.getusername()

    def getgopherURL(self):
        return 'gopher://' + urllib.quote_plus(self.gethost()) + ':' + \
               urllib.quote_plus("%d" % self.getport()) + '/' + \
               urllib.quote_plus(self.gettype()) + \
               urllib.quote_plus(self.getselector())

    def getHTMLlink(self, baseURL="hurg", about=0):
        if about:
            return self.getHTMLlink(about=0) + '&cmd=about'
        return baseURL + '?' + urllib.urlencode(self.entrydata)

    def getHTMLdirline(self, baseURL="hurg"):
        return '<A HREF="%s"><TT>%s</TT></A>' % (self.getHTMLlink(baseURL),
                                        self.getHTMLusername(0))

    def getHTMLimagetag(self, aboutlink=0):
        if self.imagemap.has_key(self.gettype()) and \
           self.imagemap[self.gettype()]:
            if aboutlink:
                return '<A HREF="' + self.getHTMLlink(about=1) + '">' + \
                       self.getHTMLimagetag(aboutlink=0) + '</A>'
            return '<IMG SRC="' + self.imagemap[self.gettype()] + '" BORDER=0>'
        else:
            return '&nbsp;'

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

    def getcontenttype(self):
        if self.typemap.has_key(self.gettype()):
            return self.typemap[self.gettype()]
        else:
            return 'text/plain'

    def display(self):
        print "Content-Type: " + self.getcontenttype()
        print
        gc = GopherComm()
        sock = gc.getdocsocket(self.gethost(), self.getport(),
                               self.getselector()).makefile()
        copy(sock, sys.stdout)

class GopherFileInfo(GopherFile):
    implementsTypes = ['i']
    
    def getHTMLdirline(self):
        return "<TT>" + re.sub(' ', '&nbsp;', self.getusername()) + "</TT>"

class GopherFileError(GopherFile):
    implementsTypes = ['3']

    def getHTMLdirline(self):
        return '&nbsp;'

class GopherFileMisc(GopherFile):
    implementsTypes = ['0', '4', '5', '9', 's', 'I', 'g', 'h']

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
        print """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
        "http://www.w3.org/TR/REC-html40/loose.dtd">"""
        print "<HTML><HEAD><TITLE>Gopher: "
        print cgi.escape(self.getusername())
        print "</TITLE></HEAD><BODY>"
        print self.getspiel()
        print "<H1>Gopher: "
        print cgi.escape(self.getusername())
        print '</H1>'
        print '<TABLE WIDTH="100%" CELLSPACING="0" CELLPADDING="0">'
        for entry in self.data:
            print "<TR><TD>" + entry.getHTMLimagetag(aboutlink=1) + "</TD>" ,
            print "<TD>&nbsp;" + entry.getHTMLdirline() ,
            ct = entry.getcontenttype()
            if ct and ct.rfind('/') > 0:
                ct = ct[ct.rfind('/')+1:]
            print '</TD><TD><FONT SIZE="-2">%s</FONT></TD></TR>' % ct 
        print "</TABLE><HR>"
        serverroot = GopherFile(self.gethost(), self.getport(),
                                '1', '', self.gethost())
        print '[<A HREF="' + serverroot.getHTMLlink() + '">server top</A>]' + \
              '&nbsp;[<A HREF="' + self.getHTMLlink(about=1) + \
              '">about</A>]&nbsp;[<A HREF="' + self.getgopherURL() + \
              '">native&nbsp;view</A>]&nbsp;' + \
              '[<A HREF="hurg?cmd=open">open</A>]<BR>'
        print 'Generated by HURG'
        print "</BODY></HTML>"


def copy(infile, outfile):
    while 1:
        line = infile.read(4096)
        if len(line) == 0: break
        outfile.write(line)
