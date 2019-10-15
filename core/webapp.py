
import os, os.path
import random
import cherrypy

import sqlite3

import hashlib
import base64
import binascii
import time


class DbHelper:
    def __init__(self,dbfile):
        self.dbfile=dbfile


    def select(self,query,params):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        if type(params) is tuple:
            cur.execute(query, params)
        else:
            cur.execute(query,(params,))
        return cur.fetchall()

    def update(self,query,params):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()

def hashpass(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password



def readFile(path):
    f = open(path, "r")
    contents = f.read()
    return contents



messages = {
    -1 : "",
     0 :  '<div class="alert alert-success" role="alert">Flag uploaded</div>',
     1 : '<div class="alert alert-danger" role="alert">User not logged</div>',
     2 : '<div class="alert alert-danger" role="alert">Invalid flag</div>',
     3 : '<div class="alert alert-danger" role="alert">Invalid user credentials</div>',
     4: '<div class="alert alert-danger" role="alert">Error - no milk today</div>',
     5: '<div class="alert alert-danger" role="alert">Error - Password not match</div>',
     6: '<div class="alert alert-danger" role="alert">Error - user defined</div>',
     7: '<div class="alert alert-danger" role="alert">User Created</div>'


}


class CoreSystem:





    def __init__(self):
        self.dbhelper = DbHelper('database.db')



    def getFlagString(self,token,userid):
        print(type(userid))
        flags = self.dbhelper.select("select chalenge from tblflags  where id not in (select id from tblflags  join tblflagsusers on id = flagid and userid =?) order by chalenge asc",userid)
        value = ""
        for flag in flags:
            value = value + '<option>'+flag[0]+'</option>'
        return value



    @cherrypy.expose
    def index(self,**args):
        msg = -1
        if 'msg' in args:
            msg = int(args["msg"])
        if 'token' in cherrypy.session.keys():
            return readFile("static/page.html").replace("FLAGIDS",self.getFlagString(cherrypy.session['token'],cherrypy.session['userid'])).replace("MESSAGE",messages[msg])
        return readFile("static/index.html").replace("MESSAGE",messages[msg])

    @cherrypy.expose
    def login(self, user, password):
        user = self.dbhelper.select("select id,uname,passwd from tblusers where uname =? ", user)
        if user is not None and len(user)>0:
             if verify_password(user[0][2],password):
                token = base64.b64encode(hashlib.sha256(str(random.randint(0, 1024)).encode("ascii")).digest()).decode('ascii')
                cherrypy.session['token'] = token
                cherrypy.session['userid'] = user[0][0]
                raise cherrypy.HTTPRedirect('/')

        raise cherrypy.HTTPRedirect('/?msg=3')

    @cherrypy.expose
    def submit(self,flagname='',flagvalue=''):
        if 'userid' not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect('/?msg=1')

        result = self.dbhelper.select("select id from tblflags where chalenge=? and flag=?",(flagname,flagvalue) )
        if (len(result)==0):
            raise cherrypy.HTTPRedirect('/?msg=2')
        flagid = result[0][0]
        userid = int(cherrypy.session['userid'])
        timestamp = int(time.time())
        self.dbhelper.update("insert into tblflagsusers values (?,?,?)",(flagid,userid,timestamp))



        raise cherrypy.HTTPRedirect('/?msg=0')

    @cherrypy.expose
    def logout(self):
        del cherrypy.session['token']
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def register(self, **args):
        msg = -1
        if 'msg' in args:
            msg = int(args["msg"])

        if (len(args)==0):
            return readFile("static/register.html").replace("MESSAGE",messages[msg])
        if ('user' in args) and ('password' in args) and ('confirm' in args):
            usr = args["user"]
            password = args["password"]
            conf = args["confirm"]
            if (password !=conf):
                raise cherrypy.HTTPRedirect('/?msg=5')
            check = self.dbhelper.select("select id,uname,passwd from tblusers where uname =? ", usr)
            print(check)
            if (len(check)!=0):
                raise cherrypy.HTTPRedirect('/?msg=6')
            hashed = hashpass(password)
            self.dbhelper.update('INSERT INTO tblusers (uname, passwd) VALUES (?,?)', (usr,hashed))
            f = open("users.txt", "a+")
            f.write(usr+":"+password+"\n")
            f.close()
            raise cherrypy.HTTPRedirect('/?msg=7')

        raise cherrypy.HTTPRedirect('/?msg=4')



    # @cherrypy.expose
    # @cherrypy.tools.json_out()
    # def data(self, pagenumber=0, search=""):
    #
    #     try:
    #         conn = sqlite3.connect("database.db")
    #         cur = conn.cursor()
    #         search = search.upper()
    #
    #         query = "SELECT * FROM tblusers where (fname like '%" + search + "%') or (sname  like '%" + search + "%') LIMIT " + str(pagenumber) +",10";
    #         print(query)
    #         cur.execute( query )
    #         rows = cur.fetchall()
    #         result = []
    #         for row in rows:
    #            result.append( {
    #               'id' : str(row[0]),
    #               'fname': row[1],
    #               'sname': row[2],
    #               'credits': row[3]
    #             })
    #         return result
    #     except Error as e:
    #         print (e)
    #         return str(e)
    #     finally:
    #         conn.close()




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
    cherrypy.quickstart(CoreSystem(), '/', conf)












