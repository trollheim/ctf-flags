
import os, os.path
import random
import string
import cherrypy
import threading
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode
browser = Firefox( executable_path='./resources/geckodriver',options=opts)
browser.get('https://duckduckgo.com')
class MyThread(threading.Thread):
    def run(self):
        print("{} started!".format(self.getName()))
        browser.get('https://duckduckgo.com')
        print("{} finished!".format(self.getName()))


def readFile(path):
    f=open(path, "r")
    contents =f.read()
    return contents



class HelloWorld(object):
    content  = "";

    @cherrypy.expose
    def index(self):
        return readFile("static/index.html").replace("CONTENT",self.content)

    @cherrypy.expose
    def form(self, msg,flag):
        self.content+=msg+"\n<br>";
        raise cherrypy.HTTPRedirect('/')

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }

    cherrypy.quickstart(HelloWorld(), '/', conf)


