import shlex
import geojson
from geojson import Feature, Point, FeatureCollection

FUEL_DIR = 'D:/steamcmd/steamapps/common/FUEL/'

with open(FUEL_DIR + 'GameTsc/Story/poi.tsc', 'r') as input:
    features_vp = []
    features_teleport = []
    for line in input:
        if line.startswith('AddTypePointOfInterest '):
            parts = line[23:].split(' ')
            print(parts)
            if parts[0] == '"VP"':
                features_vp.append(Feature(geometry=Point((float(parts[2]), float(parts[3]))), properties={"category": "vp", "trtext": int(parts[1])}))
            elif parts[0] == '"Teleport"':
                assert int(parts[1]) == 127
                features_teleport.append(Feature(geometry=Point((float(parts[2]), float(parts[3]))), properties={"category": "teleport"}))
            else:
                print(parts[0])
                assert False
    with open('docs/geo/vp.geojson', 'w') as output:
        geojson.dump(FeatureCollection(features_vp), output, separators=(',', ':'))
    with open('docs/geo/teleport.geojson', 'w') as output:
        geojson.dump(FeatureCollection(features_teleport), output, separators=(',', ':'))

with open(FUEL_DIR + 'GameTsc/Story/hubinfos.tsc', 'r') as input:
    features_livery = []
    for line in input:
        if line.startswith('AddVehicleLivery '):
            parts = shlex.split(line[17:])
            print(parts)
            if parts[4] == "ALWAYS" or parts[4] == "CHEAT":
                continue
            elif parts[4] == "POI":
                assert parts[5] == "NONE"
                features_livery.append(Feature(geometry=Point((float(parts[6]), float(parts[7]))), properties={"category": "livery", "trtext": int(parts[3])}))
            else:
                print(parts[4])
                assert False
    with open('docs/geo/livery.geojson', 'w') as output:
        geojson.dump(FeatureCollection(features_livery), output, separators=(',', ':'))

with open(FUEL_DIR + 'GameTsc/Story/miss_official.tsc', 'r') as input:
    features_career = []
    for line in input:
        if line.startswith('EMD_SetStartPos '):
            parts = line[16:].split(' ')
            print(parts)
            features_career.append(Feature(geometry=Point((float(parts[0]), float(parts[2]))), properties={"category": "career"}))
    with open('docs/geo/career.geojson', 'w') as output:
        geojson.dump(FeatureCollection(features_career), output, separators=(',', ':'))

with open(FUEL_DIR + 'GameTsc/Story/missChallenge.tsc', 'r') as input:
    features_challenge = []
    for line in input:
        if line.startswith('EMD_SetStartPos '):
            parts = line[16:].split(' ')
            print(parts)
            features_challenge.append(Feature(geometry=Point((float(parts[0]), float(parts[2]))), properties={"category": "challenge"}))
    with open('docs/geo/challenge.geojson', 'w') as output:
        geojson.dump(FeatureCollection(features_challenge), output, separators=(',', ':'))

with open(FUEL_DIR + 'GameTsc/Story/indianMissions.tsc', 'r') as input:
    features_indian = []
    for line in input:
        if line.startswith('EMD_SetStartPos '):
            parts = line[16:].split(' ')
            print(parts)
            features_indian.append(Feature(geometry=Point((float(parts[0]), float(parts[2]))), properties={"category": "indian"}))
    with open('docs/geo/indian.geojson', 'w') as output:
        geojson.dump(FeatureCollection(features_indian), output, separators=(',', ':'))
