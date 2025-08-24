import geojson
from geojson import Feature, Point, FeatureCollection, LineString, Polygon
import json
import math
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


def polygon_vertex_loop(vertices, edges, polygon_edge_indices):
    if not polygon_edge_indices:
        return []

    e0 = edges[polygon_edge_indices[0]]
    loop = [e0[0], e0[1]]
    used_edges = {polygon_edge_indices[0]}

    while len(loop) <= len(polygon_edge_indices):
        extended = False
        for i in polygon_edge_indices:
            if i in used_edges:
                continue
            v1, v2 = edges[i]
            if loop[-1] == v1:
                loop.append(v2)
                used_edges.add(i)
                extended = True
                break
            elif loop[-1] == v2:
                loop.append(v1)
                used_edges.add(i)
                extended = True
                break
            elif loop[0] == v1:
                loop.insert(0, v2)
                used_edges.add(i)
                extended = True
                break
            elif loop[0] == v2:
                loop.insert(0, v1)
                used_edges.add(i)
                extended = True
                break
        if not extended:
            raise ValueError("Edges do not form a proper loop")

    return loop


with open("docs/geo/hub.geojson", "w") as output:
    features_hub = []
    hub_coordinates = [
        [-51259.0039, 756.749207, -30274.5625],
        [-53124.6406, 555.131958, -57561.7109],
        [4697.59473, 2024.62805, -27567.916],
        [226.732132, 2133.04541, -2585.27515],
        [-53574.4688, 978.561035, 521.710632],
        [-35615.6211, 1358.85999, -2198.6936],
        [-51102.6211, 2937.83887, 32706.1699],
        [-28193.5742, 2414.4375, 46627.7031],
        [27935.8398, 1125.07043, 50224.6094],
        [47994.5977, 763.046448, 9643.90723],
        [48329.3711, 1052.4574, 29706.6641],
        [45871.6484, 1157.17212, -6269.13281],
        [18275.1504, 885.313538, 866.25531],
        [4212.21094, 1292.35449, 35516.2812],
        [40252.6211, 788.463684, -22353.3066],
        [57824.7617, 716.94574, -31062.7891],
        [50607.1992, 708.613403, -55460.8594],
        [23905.7285, 1079.2605, -50371.7266],
        [-640.231018, 4485.22363, -47690.4336],
    ]
    for hub_coordinate in hub_coordinates:
        features_hub.append(
            Feature(
                geometry=Point((hub_coordinate[0], hub_coordinate[2])),
                properties={"category": "hub"},
            )
        )
    geojson.dump(FeatureCollection(features_hub), output, separators=(",", ":"))

with open(
    USA1_DIR + "resources/$-1311324211$WhaleForceSuggest.GenWorld_Z.d/resource.json",
    "r",
) as input:
    features_zone = []
    j = json.load(input)
    body = j["class"]["GenWorld"]["GenWorldV1_381_67_09PC"]["body"]
    zone_vertices = body["region_vertices"]
    zone_edges = body["region_edges"]
    zones = body["regions"]
    print(zone_vertices)

    for name, zone in zones.items():
        vertex_indices = polygon_vertex_loop(
            zone_vertices,
            [
                [e["region_vertices_index_a"], e["region_vertices_index_b"]]
                for e in zone_edges
            ],
            zone["region_edges_indices"],
        )

        vertices = []
        for vertex_index in vertex_indices:
            vertices.append(zone_vertices[vertex_index])

        features_zone.append(
            Feature(
                geometry=Polygon([vertices]),
                properties={"category": "zone"},
            )
        )
    with open("docs/geo/zone.geojson", "w") as output:
        geojson.dump(FeatureCollection(features_zone), output, separators=(",", ":"))

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
