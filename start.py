#!/usr/bin/env python

import cherrypy
import geojson

class Schools(object):

    exposed = True

    def GET(self, id=None):

        if id == None:
            return "All Schools"
        elif id == '1':
            return "School"
        else:
            return "Not Found"

if __name__ == "__main__":

    cherrypy.tree.mount(
            Schools(), '/api/schools',
            { '/':
                {'request.dispatch' : cherrypy.dispatch.MethodDispatcher()}
            }
    )

    cherrypy.engine.start()
    cherrypy.engine.block()
