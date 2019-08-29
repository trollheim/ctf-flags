
import os, os.path

import cherrypy

import pymongo
import json

def readFile(path):
    f = open(path, "r")
    contents = f.read()
    return contents

class Flag07:

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["flagdb"]

    @cherrypy.expose
    def index(self):
        return readFile("static/index.html")

    @cherrypy.expose
    def login(self, user, password):
        query = "this.username == '" + user + "' && 'this.password' == '" + password + "'"
        if self.mydb.users.find({"$where": query}).count() > 0:
            flag = readFile("flag.txt")
            return flag
                # return "logged"
        raise cherrypy.HTTPRedirect('/')



    @cherrypy.expose
    def logout(self):
        del cherrypy.session['token']
        raise cherrypy.HTTPRedirect('/')








if __name__ == '__main__':
    conf = {


        '/res':
            {'tools.staticdir.on': True,
             'tools.staticdir.dir': "./static/res"
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
    cherrypy.quickstart(Flag07(), '/', conf)












