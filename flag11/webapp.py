import os, os.path
import random
import cherrypy
import csv
import json
import base64
from cherrypy.lib import static



def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents

class Flag11:

    @cherrypy.expose
    def index(self,**params):
        return readFile("static/index.html")


    @cherrypy.expose
    def parse(self,document):

        return "OK"








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


