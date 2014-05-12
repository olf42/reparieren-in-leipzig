#!/usr/bin/env python3

import cherrypy
import sqlite3

from geojson import Feature, Point, FeatureCollection, dumps

from mako.template import Template
from mako.lookup import TemplateLookup

import os.path

#database conf
db_name = "places.db"
db_dir = "database"
db = os.path.join(os.path.dirname(__file__), db_dir, db_name)

#geojsonfile
gj_filename = "places.geojson"
gj_dir = "public"
gj_file = os.path.join(os.path.dirname(__file__), gj_dir, gj_filename)

#template dir
temp_lookup = TemplateLookup(directories=['templates'])

#delete-link
del_link1 = "<a href='admin?del="
del_link2 = "'>Löschen</a>"

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

    def update(self):
        pass

    def delete(self, place_id):
        places.execute(''' DELETE FROM places
                           WHERE id=?''', (place_id,))
        data.commit()
        pass

    def gen_geojson(self, db_extract):
        schools = []
        for element in db_extract:
            desc = "<b>%s</b><br />%s<br /><a href='%s'>Website</a>" % (str(element[1]), str(element[2]), str(element[3]))
            school = Feature(
                    geometry=Point(
                        (float(element[4]),
                        float(element[5]))),
                    properties={
                        "name": element[0],
                        "popupContent" : desc
                        })
            schools.append(school)
            gj = FeatureCollection(schools)
            gj_fo_ = open(gj_file, 'w')

    def get_places(self):
        return places.execute(''' SELECT * FROM places''')

    def get_places_by_cat(self, cat):
        if cat in range(0,6):
            return places.execute(''' SELECT * FROM places WHERE type=?''', cat)

class Backend(object):

    @cherrypy.expose
    def index(self):
        return temp_lookup.get_template("index.html").render()

    @cherrypy.expose
    def admin(self, **kwargs):
        p_db = Places(db)
        if len(kwargs)>0:
            del_id = 0
            try:
                    del_id = kwargs["del"]
            except:
                pass
            if del_id:
                p_db.delete(del_id)
            elif len(kwargs)==6:
                place_add = (kwargs["name"],
                                kwargs["desc"],
                                kwargs["website"],
                                kwargs["long"],
                                kwargs["lat"],
                                kwargs["type"])
                p_db.add(place_add)

        #for key in kwargs:
        #    print(key, kwargs[key])

        #add delete link for every place
        places = p_db.get_places()
        places_list = []
        for row in places:
            place = []
            del_link = del_link1 + str(row[0]) + del_link2
            for element in row:
                place.append(element)
            place.append(del_link)
            places_list.append(place)
        return temp_lookup.get_template("admin.html").render(data=places_list)

    @cherrypy.expose
    def karte(object):
        return temp_lookup.get_template("karte.html").render()

    @cherrypy.expose
    def about(object):
        return temp_lookup.get_template("about.html").render()

def main():
    conf = {
        "/": {
            "tools.staticdir.root" : os.path.dirname(os.path.realpath(__file__)),
            "tools.staticdir.on" : True,
            "tools.staticdir.dir" : "public",
        },
        "/admin": {
            "tools.staticdir.root" : os.path.dirname(os.path.realpath(__file__)),
            "tools.staticdir.on" : True,
            "tools.staticdir.dir" : "public",
            "tools.digest_auth.on": True,
            "tools.digest_auth.realm": 'localhost',
            "tools.digest_auth.users": {
                "test": "test",
            }
        },
    }
    cherrypy.quickstart(Backend(), config = conf)


if __name__ == "__main__":
    main()
    #bla.add(("name", "beschreibung", "http://sublab.org", 51.33, 12.33, 2))
    #bla.delete("1")
    #bla.gen_geojson()
