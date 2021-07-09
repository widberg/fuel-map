import geojson
from geojson import Feature, Point, FeatureCollection

FUEL_DIR = 'D:/SteamLibrary/steamapps/common/FUEL/'

min_x = -65537.0
max_x = 65535.0
min_y = -65537.0
max_y = 65535.0

scale_x = 65530 / ((max_x - min_x) / 2 + 4096 + 350)
scale_y = 65530 / ((max_y - min_y) / 2 + 4096 + 350)

def normalize(val, max, min):
    return 0.5 - (val - min) / (max - min)

with open('docs/geo/poi.json', 'w') as output:
    features = []
    with open(FUEL_DIR + 'GameTsc/Story/hubinfos.tsc', 'r') as input:
        pass
    with open(FUEL_DIR + 'GameTsc/Story/poi.tsc', 'r') as input:
        for line in input:
            if line.startswith('AddTypePointOfInterest '):
                coords = line[23:].split(' ')
                features.append(Feature(geometry=Point((normalize(float(coords[2]), min_x, max_x) * scale_x, normalize(float(coords[3]), min_y, max_y) * scale_y)), properties={"icon": {"iconUrl": "https://widberg.github.io/fuel-map/img/vista.png"}}))
    with open(FUEL_DIR + 'GameTsc/Story/miss_official.tsc', 'r') as input:
        pass
        # for line in input:
        #     if line.startswith('EMD_SetStartPos '):
        #         coords = line[16:].split(' ')
        #         features.append(Feature(geometry=Point((normalize(float(coords[2]), 65535.0, -65537.0), normalize(float(coords[0]), 65535.0, -65537.0)))))
    with open(FUEL_DIR + 'GameTsc/Story/missChallenge.tsc', 'r') as input:
        pass
        # for line in input:
        #     if line.startswith('EMD_SetStartPos '):
        #         coords = line[16:].split(' ')
        #         features.append(Feature(geometry=Point((normalize(float(coords[2]), 65535.0, -65537.0), normalize(float(coords[0]), 65535.0, -65537.0)))))
    data = geojson.dumps(FeatureCollection(features))
    output.write(data)
