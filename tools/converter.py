#!/usr/bin/env python

import csv
from geojson import Feature, Point, FeatureCollection, dumps

schools = []

with open('places.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for element in reader:
        school = Feature(
                geometry=Point(
                    (float(element[2].lstrip()),
                    float(element[3].lstrip()))),
                properties={
                    "name": element[0],
                    "popupContent" : element[1]
                    })
        schools.append(school)

print(FeatureCollection(schools))
