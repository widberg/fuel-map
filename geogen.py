import geojson
from geojson import Feature, Point, FeatureCollection, LineString
import json
import shlex

FUEL_DIR = "D:/steamcmd/steamapps/common/FUEL/"
USA1_DIR = "D:/programming/widberg/bff/data/USA1.DPC.rich.d/"

with open(FUEL_DIR + "GameTsc/Story/poi.tsc", "r") as input:
    features_vp = []
    features_teleport = []
    for line in input:
        if line.startswith("AddTypePointOfInterest "):
            parts = line[23:].split(" ")
            print(parts)
            if parts[0] == '"VP"':
                features_vp.append(
                    Feature(
                        geometry=Point((float(parts[2]), float(parts[3]))),
                        properties={"category": "vp", "trtext": int(parts[1])},
                    )
                )
            elif parts[0] == '"Teleport"':
                assert int(parts[1]) == 127
                features_teleport.append(
                    Feature(
                        geometry=Point((float(parts[2]), float(parts[3]))),
                        properties={"category": "teleport"},
                    )
                )
            else:
                print(parts[0])
                assert False
    with open("docs/geo/vp.geojson", "w") as output:
        geojson.dump(FeatureCollection(features_vp), output, separators=(",", ":"))
    with open("docs/geo/teleport.geojson", "w") as output:
        geojson.dump(
            FeatureCollection(features_teleport), output, separators=(",", ":")
        )

with open(FUEL_DIR + "GameTsc/Story/hubinfos.tsc", "r") as input:
    features_livery = []
    for line in input:
        if line.startswith("AddVehicleLivery "):
            parts = shlex.split(line[17:])
            print(parts)
            if parts[4] == "ALWAYS" or parts[4] == "CHEAT":
                continue
            elif parts[4] == "POI":
                assert parts[5] == "NONE"
                features_livery.append(
                    Feature(
                        geometry=Point((float(parts[6]), float(parts[7]))),
                        properties={"category": "livery", "trtext": int(parts[3])},
                    )
                )
            else:
                print(parts[4])
                assert False
    with open("docs/geo/livery.geojson", "w") as output:
        geojson.dump(FeatureCollection(features_livery), output, separators=(",", ":"))

with open(FUEL_DIR + "GameTsc/Story/miss_official.tsc", "r") as input:
    features_career = []
    features_hidden = []
    name = ""
    for line in input:
        if line.startswith("EMD_SetName "):
            name = line[12:].strip()
        elif line.startswith("EMD_SetStartPos "):
            parts = line[16:].split(" ")
            print(parts)
            if name in ['"CR42-Chec-BJ"', '"CR_Tutotest1"', '"CR_Tutotest2"']:
                features_hidden.append(
                    Feature(
                        geometry=Point((float(parts[0]), float(parts[2]))),
                        properties={"category": "hidden"},
                    )
                )
            else:
                features_career.append(
                    Feature(
                        geometry=Point((float(parts[0]), float(parts[2]))),
                        properties={"category": "career"},
                    )
                )
    with open("docs/geo/career.geojson", "w") as output:
        geojson.dump(FeatureCollection(features_career), output, separators=(",", ":"))
    with open("docs/geo/hidden.geojson", "w") as output:
        geojson.dump(FeatureCollection(features_hidden), output, separators=(",", ":"))

with open(FUEL_DIR + "GameTsc/Story/missChallenge.tsc", "r") as input:
    features_challenge = []
    for line in input:
        if line.startswith("EMD_SetStartPos "):
            parts = line[16:].split(" ")
            print(parts)
            features_challenge.append(
                Feature(
                    geometry=Point((float(parts[0]), float(parts[2]))),
                    properties={"category": "challenge"},
                )
            )
    with open("docs/geo/challenge.geojson", "w") as output:
        geojson.dump(
            FeatureCollection(features_challenge), output, separators=(",", ":")
        )

with open(FUEL_DIR + "GameTsc/Story/indianMissions.tsc", "r") as input:
    features_indian = []
    for line in input:
        if line.startswith("EMD_SetStartPos "):
            parts = line[16:].split(" ")
            print(parts)
            features_indian.append(
                Feature(
                    geometry=Point((float(parts[0]), float(parts[2]))),
                    properties={"category": "indian"},
                )
            )
    with open("docs/geo/indian.geojson", "w") as output:
        geojson.dump(FeatureCollection(features_indian), output, separators=(",", ":"))

with open(
    USA1_DIR + "resources/$-392451512$EmpowerHugeViolin.GwRoad_Z.d/resource.json", "r"
) as input:
    features_road = []
    j = json.load(input)
    roads = j["class"]["GwRoad"]["GwRoadV1_381_67_09PC"]["body"]["roads"]
    print(f"{len(roads)} roads")
    for road in roads:
        features_road.append(
            Feature(
                geometry=LineString(road["points"]),
                properties={"category": "road"},
            )
        )
    with open("docs/geo/road.geojson", "w") as output:
        geojson.dump(FeatureCollection(features_road), output, separators=(",", ":"))
