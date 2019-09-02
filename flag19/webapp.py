import os, os.path
import random
import cherrypy
import csv
import subprocess
import cherrypy_cors

cherrypy_cors.install()


# ', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents





class Flag18:

    @cherrypy.expose
    def index(self):
        return readFile("static/page.html")



    @cherrypy.expose
    def imgserve(self,src):
       path = os.path.join(absDir, src)
       return cherrypy.lib.static.serve_download(path)







if __name__ == '__main__':



    conf = {

        '/res':
            {'tools.staticdir.on': True,
             'tools.staticdir.dir':  "./static/res"
             },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'cors.expose.on': True,

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


