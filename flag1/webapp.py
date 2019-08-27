import os, os.path
import random
import cherrypy
import csv


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

with open('users.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=':')
    for row in csv_reader:
        users.append(User(row[0],row[1]))


class Flag01:



    def _cp_dispatch(self, vpath):

        if len(vpath) == 2 and  vpath.pop(0) == 'bot':
            cherrypy.request.params['userid'] = vpath.pop(0)

        return vpath

    @cherrypy.expose
    def bot(self, userid):
        user = users[int(userid)]
        return readFile("static/bot.html").replace("CONTENT", user.content)

    @cherrypy.expose
    def index(self):
        if 'token' in cherrypy.session.keys():
            user = self.findUser()
            return readFile("static/page.html").replace("CONTENT",user.content)
        return readFile("static/index.html")


    @cherrypy.expose
    def login(self,user,password):
        for u in users:
            if u.user == user and u.password == password:
                cherrypy.session['token'] = u.token
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

    @cherrypy.expose
    def form(self, msg,flag):
        user = self.findUser()
        user.content = '<div class="alert alert-info" role="alert">' +msg +'</div>' + user.content
        raise cherrypy.HTTPRedirect('/')





    @cherrypy.expose
    def bform(self, msg,flag):
        for user in users:
            user.content+= '<div class="alert alert-info" role="alert">' +msg +'</div>';
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
    cherrypy.quickstart(Flag01(), '/', conf)


