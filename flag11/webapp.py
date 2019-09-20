import os, os.path

import cherrypy
from xml.etree.ElementTree import fromstring

from xml.etree.ElementTree import ParseError
import multiprocessing


def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents


def parse(document,q):
    try:
        fromstring(document)
        q.put(True)
    except ParseError as e:
        print("Error")
        print(e)
        q.put(False)


class Flag11:

    @cherrypy.expose
    def index(self,**params):
        return readFile("static/index.html")

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def parse(self,xmldocument):
        if len (xmldocument)>1024:
            return "File is too big"

        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=parse, name="XMLParse", args=(xmldocument,q))
        p.start()
        p.join(10)

        if p.is_alive():
            try:
                p.terminate()
                p.kill()
                p.join()
            except:
                pass
            return readFile("flag.txt")

        if q.get() != True:
            return "Error processing data"
        return "OK"








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
    cherrypy.quickstart(Flag11(), '/', conf)


