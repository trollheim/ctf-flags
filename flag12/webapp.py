import os, os.path
import random
import cherrypy
import csv
import json
import base64
import hmac
import hashlib
import base64


# dig = hmac.new(b'1234567890', msg=your_bytes_string, digestmod=hashlib.sha256).digest()
# base64.b64encode(dig).decode()      # py3k-mode
# 'Nace+U3Az4OhN7tISqgs1vdLBHBEijWcBeCqL5xN9xg='

# "alg": "HS256",
# "typ": "JWT"
class JWT:


    def verify(self,  msg,sign,secret,alg):
        sig_bytes = base64.urlsafe_b64decode(sign);
        sig_ver = self.sign(msg,secret,alg)
        return sig_bytes ==  base64.urlsafe_b64decode(sig_ver)


    def sign(self, payload, secret, alg):
        if alg.lower()=='hs256':
            print("xxx")
            print(payload)
            dig = hmac.new(secret, msg=payload.encode("ascii"), digestmod=hashlib.sha256).digest()
            return base64.b64encode(dig).decode();
        if alg.lower()=='none':
            return ''

    def encode(self,body,alg,secret):
        header = { 'alg': alg, "typ": "JWT"}
        h=base64.urlsafe_b64encode( json.dumps(header).encode("ascii")).decode("ascii")

        jsonStr = json.dumps(body);
        b=base64.urlsafe_b64encode( jsonStr.encode("ascii")).decode("ascii")
        payload = h+"."+b
        print(payload)

        return payload+"."+self.sign(payload,secret,alg)

    def decode(self,token,secret):
        parts = token.split(".")
        if len(parts)!=3:
            return (False,None)
        tokenb64 = base64.b64decode(parts[0])
        header = json.loads(tokenb64)
        alg = header['alg']
        if (self.verify(parts[0]+'.'+parts[1],parts[2],secret,alg)):
            return (True,json.loads(base64.b64decode(parts[1])))
        return (False, None)

SECRET = hashlib.sha256(str(random.randint(0, 1024)).encode("ascii")).digest()


class User:
    def __init__(self,user,password):
        self.user = user
        self.password = password

        token = {'token':  hashlib.sha256(str(random.randint(0, 1024)).encode("ascii")).hexdigest(), 'userid' : 42, 'admin': False}
        self.token = JWT().encode(token,'hs256',SECRET)





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

            print(cherrypy.request.cookie['token'].value[0])
            cookie = cherrypy.request.cookie
            jws = cookie['token'].value
            result = JWT().decode(jws,SECRET)
            if result[0]==False:
                return readFile("static/index.html")
            token = result[1]
            content = "Log in as admin to get flag"
            if token["userid"]!= 42:
                content = "You wish...."
            if token['admin']:
                content = readFile("flag.txt")

            return readFile("static/page.html").replace("CONTENT",content );
        return readFile("static/index.html")


    @cherrypy.expose
    def login(self,user,password):
        for u in users:
            if u.user == user and u.password == password:
                cookie = cherrypy.response.cookie

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


