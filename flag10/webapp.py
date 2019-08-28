import os, os.path
import random
import cherrypy
import csv
import json
import base64
from cherrypy.lib import static


class User:
    def __init__(self,user,password):
        self.user = user
        self.password = password
        self.token = hash((self, random.randint(0, 1024)))



    def validate(self,usr,pwd):
        return self.user == usr and self.password == pwd


    content = "";


def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents

users = []

with open('users.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=':')
    for row in csv_reader:
        print(row)
        users.append(User(row[0],row[1]))

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

class Flag10:

    @cherrypy.expose
    def index(self,**params):
        return readFile("static/index.html")


    @cherrypy.expose
    def data(self):
        path = os.path.join(absDir, 'hackedusers.txt')
        return static.serve_download(path)

    @cherrypy.expose
    def dict(self):
        path = os.path.join(absDir, "./data/passwords.txt")
        return static.serve_download(path)

    @cherrypy.expose
    def readme(self):
        cherrypy.response.headers['Content-Type'] = "text/plain"
        cherrypy.response.headers['Content-Disposition'] = "attachment; filename=readme.txt"
        return "HAIL HYDRA!!!"


    @cherrypy.expose
    def login(self,user,password):
        for u in users:
            if u.user == user:
                if u.password == password:
                    flag = readFile("flag.txt")
                    return flag
            raise cherrypy.HTTPRedirect('/?error=2')


        raise cherrypy.HTTPRedirect('/?error=1')



    @cherrypy.expose
    def logout(self):
        try:
            del cherrypy.session['token']
        except:
            print("error")
        raise cherrypy.HTTPRedirect('/')


    def findUser(self):
        token = cherrypy.session['token'];

        for u in users:
            if u.token == token:
                return u;
        del cherrypy.session['token']
        del cherrypy.response.cookie['token']
        raise cherrypy.HTTPRedirect('/')



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
    cherrypy.quickstart(Flag10(), '/', conf)


