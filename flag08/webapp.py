import os, os.path
import random
import cherrypy
import csv
import json
import base64

class User:
    def __init__(self,user,password):
        self.user = user
        self.password = password
        token = json.dumps({'token':  str(hash((self,  random.randint(0,1024)))), 'admin': False})

        self.token = str(base64.b64encode(token.encode("utf-8")),"utf-8")
        print(self.token[0]+" "+self.token)



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


class Flag08:

    @cherrypy.expose
    def index(self):
        if 'token' in  cherrypy.session.keys():
            print("tok")
            print(cherrypy.request.cookie['token'].value[0])
            cookie = cherrypy.request.cookie

            tokenb64 = base64.b64decode(cookie['token'].value)
            token = json.loads(tokenb64)
            content = "Log in as admin to get flag"
            if token['admin']:
                content = readFile("flag.txt")

            return readFile("static/page.html").replace("CONTENT",content );
        return readFile("static/index.html")


    @cherrypy.expose
    def login(self,user,password):
        for u in users:
            if u.user == user and u.password == password:
                cookie = cherrypy.response.cookie
                print(u.token)
                print(type(u.token))
                cookie['token'] = u.token
                cookie['token']['path'] = '/'
                cookie['token']['max-age'] = 3600
                cookie['token']['version'] = 1

                cherrypy.session['token'] = u.token
                # return "logged"
        raise cherrypy.HTTPRedirect('/')



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
    cherrypy.quickstart(Flag08(), '/', conf)


