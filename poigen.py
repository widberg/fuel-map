import geojson
from geojson import Feature, Point, FeatureCollection

FUEL_DIR = 'D:/SteamLibrary/steamapps/common/FUEL/'

def normalize(val, max, min):
    return 0.5 - (val - min) / (max - min)

with open('docs/geo/poi.json', 'w') as output:
    features = []
    with open(FUEL_DIR + 'GameTsc/Story/hubinfos.tsc', 'r') as input:
        pass
    with open(FUEL_DIR + 'GameTsc/Story/poi.tsc', 'r') as input:
        pass
    with open(FUEL_DIR + 'GameTsc/Story/miss_official.tsc', 'r') as input:
        for line in input:
            if line.startswith('EMD_SetStartPos '):
                coords = line[16:].split(' ')
                features.append(Feature(geometry=Point((normalize(float(coords[1]), 65535.0, -65537.0), normalize(float(coords[0]), 65535.0, -65537.0)))))
    with open(FUEL_DIR + 'GameTsc/Story/missChallenge.tsc', 'r') as input:
        pass
    data = geojson.dumps(FeatureCollection(features))
    output.write(data)
