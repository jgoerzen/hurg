# $Id: GopherComm.py,v 1.5 2001/08/29 05:46:22 jgoerzen Exp $

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

from socket import *

class GopherComm:
    def __init__(self):
        self.VERSION = '$Id: GopherComm.py,v 1.5 2001/08/29 05:46:22 jgoerzen Exp $'
    
    def getdocsocket(self, host, port=70, selector=""):
        socket = self.connectTCP(host, port)
        socket.send(selector + "\r\n")
        return socket

    def connectTCP(self, host, port):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        return s
