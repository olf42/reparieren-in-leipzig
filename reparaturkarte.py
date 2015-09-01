#!/usr/bin/env python3

import cherrypy
import sqlite3
import urllib.request
import json

from geojson import Feature, Point, FeatureCollection, dumps

from mako.template import Template
from mako.lookup import TemplateLookup

import os.path
from os import rename

#import user credentials
import credentials

#database conf
db_name = "places.db"
db_dir = "database"
db = os.path.join(os.path.dirname(__file__), db_dir, db_name)

#geojsonfile
gj_filename = "_places.json"
gj_dir = "public"

#template dir
temp_lookup = TemplateLookup(directories=['templates'])

#config file
conf_name = "reparaturkarte.config"

#delete-link
del_link1 = "<a href='admin?del="
del_link2 = "'>Löschen</a>"

#extension for temporary files
tmp_ext = ".tmp"

#categories
categories = { 0 : "Technik",
                1 : "Fahrrad",
                2 : "Textil",
                3 : "Holz",
                4 : "Sonstiges",
                5 : "Auto",
                6 : "Schuhe"}

#nominatim url for address -> coordinates matching
nominatim_url = "http://nominatim.openstreetmap.org/search?format=json&q="

class Places(object):

    def __init__(self, db):
            global data
            data = sqlite3.connect(db)
            global places
            places = data.cursor()
            places.execute(''' CREATE TABLE IF NOT EXISTS places
                             ( id integer PRIMARY KEY,
                               name text,
                               description text,
                               website text,
                               longitude real,
                               latitude real,
                               type integer

                               ) ''')
            data.commit()

    def add(self, place):
        places.execute(''' INSERT INTO places 
                         ( name, description, 
                           website, longitude, 
                           latitude, type) 
                         VALUES 
                         ( ?, ?, 
                           ?, ?, 
                           ?, ? )''', place)
        data.commit()
        self.gen_geojson()

    def update(self):
        pass

    def delete(self, place_id):
        try:
            places.execute(''' DELETE FROM places
                           WHERE id=?''', (place_id,))
        except:
            raise
        data.commit()
        self.gen_geojson()

    def gen_geojson(self):

        #fetch dataset for each category
        for cat in categories:
            places = []
            db_extract = self.get_places_by_cat(cat)

            #Create GeoJSON-Feature for each place
            for element in db_extract:
                desc = """<b>%s</b><br />
                        %s<br />
                        <a href='%s' target='_blank'>Website</a>""" % (str(element[1]),
                                                                     str(element[2]),
                                                                     str(element[3]))
                place = Feature(
                    geometry=Point(
                        (float(element[4]),
                        float(element[5]))),
                    properties={
                        "name": element[0],
                        "popupContent" : desc
                        })
                places.append(place)
            #Create FeatureCollection for each category
            gj = FeatureCollection(places)
            #target filename
            gj_file = os.path.join(os.path.dirname(__file__),
                                    gj_dir,
                                    categories[cat] + gj_filename)
            gj_fo = open(gj_file+tmp_ext, 'w+')
            gj_fo.write(str(gj))
            gj_fo.close()
            os.rename(gj_file+tmp_ext, gj_file)

    def get_places(self):
        result = places.execute(''' SELECT * FROM places''')
        #convert tuple of tuples to list of lists
        result = [list(line) for line in result]
        return result

    def get_places_by_cat(self, cat):
        if cat in range(0,7):
            return places.execute(''' SELECT * FROM places WHERE type=?''', (cat,))

class Backend(object):

    @cherrypy.expose
    def index(self):
        return temp_lookup.get_template("index.html").render()

    @cherrypy.expose
    def admin(self, **kwargs):
        error = ""
        p_db = Places(db)

        #update all geojson files to current state in DB
        p_db.gen_geojson()

        #work with given parameters
        if len(kwargs)>0:
            del_id = 0
            try:
                del_id = kwargs["del"]
            except:
                error = "Keyword not found!"
            if del_id:
                try:
                    p_db.delete(del_id)
                except:
                    error = "Error deleting Place"
            elif len(kwargs)==6:
                place_add = (kwargs["name"],
                                kwargs["desc"],
                                kwargs["website"],
                                kwargs["long"],
                                kwargs["lat"],
                                kwargs["type"])
                p_db.add(place_add)

        #use this for debugging
        #for key in kwargs:
        #    print(key, kwargs[key])

        #add delete link for every place, and replace cat-id by string
        places = p_db.get_places()
        for row in places:
            del_link = del_link1 + str(row[0]) + del_link2
            row.append(del_link)
            row[6] = categories[row[6]]
        return temp_lookup.get_template("admin.html").render(data=places, error=error)

    @cherrypy.expose
    def adminmap(self, **kwargs):
        if len(kwargs)>0:
            try:
                query = kwargs["q"]
            except:
                return "Invalid Request <a href='/adminmap'>Zurück</a>"
            if (query == "enter"):
                return(kwargs["lon"], kwargs["lat"])
        return temp_lookup.get_template("adminmap.html").render()

    @cherrypy.expose
    def adminenter(self, **kwargs):
        lat = 0
        lon = 0
        if len(kwargs)>0:
            try:
                query = kwargs["q"]
                lon = kwargs["lon"]
                lat = kwargs["lat"]
            except:
                pass
        return temp_lookup.get_template("adminenter.html").render(lat=lat, lon=lon)

    @cherrypy.expose
    def admingeojson(self, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        places = []
        if len(kwargs)>0:
            try:
                address = kwargs["address"]
                query = kwargs["q"]
            except:
                # No valid request, so we return an empty FC
                return str(FeatureCollection(places)).encode('utf-8')

            # Make a Nominatim-Request and generate geoJSON-File from it
            if (query == "search"):

                request_url = nominatim_url + address.replace(' ', '+')
                request_url = request_url.encode('ascii', 'xmlcharrefreplace').decode('ascii')

                with urllib.request.urlopen(request_url, timeout=5) as response:
                    nom_response = response.read()
                coordinates = json.loads(nom_response.decode("utf-8"))

                for element in coordinates:
                    name = element["display_name"]
                    lat = float(element["lat"])
                    lon = float(element["lon"])
                    #desc = """{0}<br/>
                    #        <b>Lon:</b>&nbsp;{1}<br/>
                    #        <b>Lat:</b>&nbsp;{2}""".format(name, lon, lat)
                    desc = """{0}<br/>
                            <b>Lon:</b>&nbsp;{1}<br/>
                            <b>Lat:</b>&nbsp;{2}<br/>
                            <a href='/adminenter?q=enter&lon={1}&lat={2}'>
                            Eintragen</a>""".format(name, lon, lat)
                    place = Feature(geometry=Point((lon, lat)),
                                             properties={
                                                    "name": coordinates.index(element),
                                                    "popupContent" : desc
                                                    })
                    places.append(place)

        # return empty for invalid request, or no matched object, or FC if successful
        return str(FeatureCollection(places)).encode('ascii', 'xmlcharrefreplace')

    @cherrypy.expose
    def karte(object):
        return temp_lookup.get_template("karte.html").render()

    @cherrypy.expose
    def embed(object):
        return temp_lookup.get_template("embed.html").render()


    @cherrypy.expose
    def list(object):
        p_db = Places(db)
        places = p_db.get_places()
        return temp_lookup.get_template("liste.html").render(data=places)

    @cherrypy.expose
    def more(object):
        return temp_lookup.get_template("more.html").render()

    @cherrypy.expose
    def about(object):
        return temp_lookup.get_template("about.html").render()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))

    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8023,
        'server.thread_pool_max': 500,
        'server.thread_pool': 100,
        'log.screen': True
    })

    cherrypy.tree.mount(Backend(), '/', {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(current_dir, 'public'),
        },
        '/admin': {
            "tools.staticdir.dir" : os.path.join(current_dir, 'public'),
            "tools.staticdir.on" : True,
            "tools.digest_auth.on": True,
            "tools.digest_auth.realm": 'localhost',
            "tools.digest_auth.users": credentials.users
        },
        '/adminmap': {
            "tools.staticdir.dir" : os.path.join(current_dir, 'public'),
            "tools.staticdir.on" : True,
            "tools.digest_auth.on": True,
            "tools.digest_auth.realm": 'localhost',
            "tools.digest_auth.users": credentials.users
        }
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
