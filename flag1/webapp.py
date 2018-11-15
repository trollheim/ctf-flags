
import os, os.path

import cherrypy



def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents



class HelloWorld(object):
    content  = "";

    @cherrypy.expose
    def index(self):
        return readFile("static/index.html").replace("CONTENT",self.content)

    @cherrypy.expose
    def form(self, msg,flag):
        self.content+=msg+"\n<br>";
        raise cherrypy.HTTPRedirect('/')

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }

    cherrypy.quickstart(HelloWorld(), '/', conf)


