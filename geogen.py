import geojson
from geojson import Feature, Point, FeatureCollection, LineString, Polygon
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

with open("docs/geo/waterbody.geojson", "w") as output:
    features_water = []
    # 0x006FFDD0
    for x, h, z, r in [
        # stock_lakes_100
        [410.0, 1770.0, 1683.0, 7000.0],
        [-50480.0, 755.0, -24970.0, 7000.0],
        [-35408.0, 700.0, -29217.0, 7000.0],
        [49250.0, 760.0, 9033.0, 16000.0],
        [-56250.0, 960.0, -530.0, 14000.0],
        [-39600.0, 1595.0, 26050.0, 7000.0],
        [-13900.0, 1350.0, 46000.0, 9000.0],
        [-60000.0, 550.0, -60000.0, 12000.0],
    ]:
        features_water.append(
            Feature(
                geometry=Polygon(
                    [
                        [
                            [x - r, z - r],
                            [x - r, z + r],
                            [x + r, z + r],
                            [x + r, z - r],
                            [x - r, z - r],
                        ]
                    ]
                ),
                properties={"category": "waterbody"},
            )
        )
    geojson.dump(FeatureCollection(features_water), output, separators=(",", ":"))

with open("docs/geo/pool.geojson", "w") as output:
    features_water = []
    # 0x006FFDD0
    for x, h, z, r in [
        # stock_lakes_sradius_0_0_625
        [-27039.0, 787.0, -28552.0, 100.0],
        [-27450.0, 785.0, -28500.0, 130.0],
        [-27394.0, 779.0, -28697.0, 100.0],
        [-58354.68, 979.19, 2106.0901, 100.0],
        [-58166.539, 976.64001, 1948.2, 100.0],
        [-58093.379, 981.81, 1596.13, 100.0],
        [-57740.191, 972.60999, 940.78998, 100.0],
        [-57511.551, 965.54999, 880.25, 100.0],
        [-57509.59, 960.23999, 642.73999, 100.0],
        [-57462.629, 960.85999, 419.54999, 100.0],
        [-57274.5, 959.53998, 536.01001, 100.0],
    ]:
        features_water.append(
            Feature(
                geometry=Polygon(
                    [
                        [
                            [x - r, z - r],
                            [x - r, z + r],
                            [x + r, z + r],
                            [x + r, z - r],
                            [x - r, z - r],
                        ]
                    ]
                ),
                properties={"category": "pool"},
            )
        )
    geojson.dump(FeatureCollection(features_water), output, separators=(",", ":"))
