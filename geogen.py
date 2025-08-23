import geojson
from geojson import Feature, Point, FeatureCollection

FUEL_DIR = 'D:/steamcmd/steamapps/common/FUEL/'

with open('docs/geo/poi.json', 'w') as output:
    features = []
    with open(FUEL_DIR + 'GameTsc/Story/poi.tsc', 'r') as input:
        for line in input:
            if line.startswith('AddTypePointOfInterest '):
                coords = line[23:].split(' ')
                features.append(Feature(geometry=Point((float(coords[2]), float(coords[3]))), properties={"category": "vista"}))
    geojson.dump(FeatureCollection(features), output)
