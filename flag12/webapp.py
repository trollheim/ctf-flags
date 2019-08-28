import os, os.path

import cherrypy
import xml.sax
from io import StringIO

def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents


class MyHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.result = ""
        self.depth = 0

    def startElement(self, name, attrs):
        self.chars = ""
        self.depth =  self.depth+1
    def characters(self, content):
        self.chars += content
    def endElement(self, name):
        self.depth = self.depth -1
        element = ""
        for i in range(self.depth):
            element = element+ " "
        element = element+ name+" = "+self.chars+" <br>"
        self.result=self.result+element


class Flag11:

    @cherrypy.expose
    def index(self,**params):
        return readFile("static/index.html")


    @cherrypy.expose
    def parse(self,document):
        handler = MyHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.setFeature(xml.sax.handler.feature_external_ges, 1)
        parser.parse(StringIO(document))
        return handler.result










if __name__ == '__main__':



    conf = {
        '/res':
            {'tools.staticdir.on': True,
             'tools.staticdir.dir':  "./static/res"
             },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            # 'tools.auth_basic.checkpassword': validate_password,

        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Flag11(), '/', conf)


