import os, os.path
import random
import cherrypy
from cherrypy._cpdispatch import Dispatcher


class User:


    def __init__(self,user,password):
        self.user = user
        self.password = password
        self.token = hash((self,  random.randint(0,1024)))



    def validate(self,usr,pwd):
        return self.user == usr and self.password == pwd


    content = "";


def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents

users = []
users.append(User( 'admin',  'W5UVa54FaZ5Ux==k%2bbT$XF@a%rsua3dQk^WPXPGLkZb_gucK+_BCvk#+w8Z9Jc'))





class Flag16:

    @cherrypy.expose
    def index(self,**args):
        if 'token' in cherrypy.session.keys():
            return readFile("flag.txt")
        return readFile("static/index.html")


    @cherrypy.expose
    def login(self,user,password):
        for u in users:
            if u.user == user and u.password == password:
                cherrypy.session['token'] = u.token
                raise cherrypy.HTTPRedirect('/')
                # return "logged"
        raise cherrypy.HTTPRedirect('/')


    @cherrypy.expose
    def logout(self):
        del cherrypy.session['token']
        raise cherrypy.HTTPRedirect('/')


    def findUser(self):
        token = cherrypy.session['token'];

        for u in users:
            if u.token == token:
                return u;
        del cherrypy.session['token']
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose(["tests.py"])
    def filerequest(self):
        return readFile("testfile.py")




if __name__ == '__main__':
    print (os.path.abspath(os.getcwd())+ '/git/index.html')
    conf = {
        '/.git': {
            'tools.staticdir.on': True,
            'tools.staticdir.index': 'index.html',
            'tools.staticdir.dir': './git'



        },
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
    cherrypy.quickstart(Flag16(), '/', conf)


