import os, os.path
import random
import cherrypy
import csv


class User:


    def __init__(self,user,password,data):
        self.user = user
        self.password = password
        self.data = data
        self.token = hash((self,  random.randint(0,1024)))
        self.id = -1


    def validate(self,usr,pwd):
        return self.user == usr and self.password == pwd


    content = "";


def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents

users = []
users.append(User("admin", str(random.randint(0,1024**3)), readFile("flag.txt")))
with open('users.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=':')
    for row in csv_reader:
        users.append(User(row[0],row[1],"Can you get admin account details?" ))
        random.shuffle(users)

random.shuffle(users)
for i in range(0,len(users)):
    users[i].id = i+1



class Flag14:

    @cherrypy.expose
    def index(self,**args):
        if 'token' in cherrypy.session.keys():
            user = self.findUser()
            replace = ''
            try:
                if 'user' in args.keys():
                    uid = int(args['user'])
                    replace = users[uid-1].data
            except:
                replace = "Error 131 - Userdata not found"


            return readFile("static/page.html").replace("CONTENT",replace)
        return readFile("static/index.html")


    @cherrypy.expose
    def login(self,user,password):
        for u in users:
            if u.user == user and u.password == password:
                cherrypy.session['token'] = u.token
                raise cherrypy.HTTPRedirect('/?user='+str(u.id))
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
    cherrypy.quickstart(Flag14(), '/', conf)


