
import os, os.path
import random
import cherrypy
import csv
import sqlite3
from sqlite3 import Error

class User:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.token = hash((self, random.randint(0, 1024)))

    def validate(self, usr, pwd):
        return self.user == usr and self.password == pwd



    content = "";


def readFile(path):
    f = open(path, "r")
    contents = f.read()
    return contents


users = []

with open('users.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=':')
    for row in csv_reader:
        users.append(User(row[0], row[1]))


class Flag06:

    def filter(self, str):
        return ''.join(filter(lambda x: not (x.isspace() or x.isalpha()), str))

    @cherrypy.expose
    def index(self):
        if 'token' in cherrypy.session.keys():
            user = self.findUser()
            return readFile("static/page.html")
        return readFile("static/index.html")

    @cherrypy.expose
    def login(self, user, password):
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
    @cherrypy.tools.json_out()
    def data(self, pagenumber=0, search=""):

        try:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            search = search.replace(" ", "%").upper()

            query = "SELECT * FROM tblusers where (fname like '%" + search + "%') or (sname  like '%" + search + "%') LIMIT " + str(pagenumber) +",10";
            print(query)
            cur.execute( query )
            rows = cur.fetchall()
            result = []
            for row in rows:
                 result.append( {
                    'id' : str(row[0]),
                    'fname': row[1],
                    'sname': row[2],
                    'credits': row[3]
                })
            print(result)
            return result



        except Error as e:
            print (e)
            return str(e)
        finally:
            conn.close()




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
    cherrypy.quickstart(Flag06(), '/', conf)












