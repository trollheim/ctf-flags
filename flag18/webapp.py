import os, os.path
import random
import cherrypy
import csv
import subprocess
# import cherrypy_cors
#
# cherrypy_cors.install()


# ', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)



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





class Flag18:

    @cherrypy.expose
    def index(self,**args):
        if 'token' in cherrypy.session.keys():
            user = self.findUser()
            return readFile("static/page.html").replace("CONTENT",'false')
        return readFile("static/index.html")

    @cherrypy.expose
    # @cherrypy.tools.accept(media="application/x-www-form-urlencoded")
    # @cherrypy.tools.json_in()
    def execute(self,mode='', *args, **post):

        param = post['param']
        b=subprocess.check_output(["ping -c4  172.17.0."+param], shell =True)
        # b = subprocess.check_output(["ping -c4  127.0.0." + param], shell=True)
        return b


    @cherrypy.expose
    def login(self,user,password):
        for u in users:
            if u.user == user and u.password == password:
                cherrypy.session['token'] = u.token
                raise cherrypy.HTTPRedirect('/')
                # return "logged"
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def admin(self):
        return readFile("static/admin.html")


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
            # 'cors.expose.on': True,

            # 'tools.auth_basic.checkpassword': validate_password,

        },

        '/robot.txt' : {
        'tools.staticfile.on' : True,

        'tools.staticfile.filename' :  os.path.abspath(os.getcwd())+"/static/robot.txt"

    },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'

        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'response.timeout': 30,
              'tools.json_in.force': False
    })
    cherrypy.quickstart(Flag18(), '/', conf)


