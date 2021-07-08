def normalize(val, max, min):
    return 0.5 - (val - min) / (max - min)

with open('roads.txt', 'r') as input:
    with open('docs/roads.js', 'w') as out:
        out.write('window.roads = [')
        lines = input.readlines()
        i = 0
        first = True
        while i < len(lines):
            if lines[i].startswith('Road '):
                configuration = lines[i][5:].split(' ')
                road_type = int(configuration[0])
                polyline_node_len = int(configuration[1])
                polyline = lines[i + 1].split(' ')
                if True:
                    if not first:
                        out.write(',')
                    else:
                        first = False
                    out.write('[')
                    for x in range(0, polyline_node_len):
                        out.write('{{lat:{},lng:{}}}'.format(normalize(float(polyline[2 * x + 1]), gen_road_min_y, gen_road_max_y) * scale_y, normalize(float(polyline[2 * x]), gen_road_min_x, gen_road_max_x) * scale_x))
                        if x < polyline_node_len - 1:
                            out.write(',')
                    out.write(']')
                i += 2
            elif lines[i].startswith('GenRoadMin '):
                gen_road_min = lines[i][11:].split(' ')
                gen_road_min_x = float(gen_road_min[0])
                gen_road_min_y = float(gen_road_min[1])
                i += 1
            elif lines[i].startswith('GenRoadMax '):
                gen_road_max = lines[i][11:].split(' ')
                gen_road_max_x = float(gen_road_max[0])
                gen_road_max_y = float(gen_road_max[1])
                scale_x = 65530 / (gen_road_max_x + 4096)
                scale_y = 65530 / (gen_road_max_y + 4096)
                i += 1
            else:
                i += 1
        out.write('];')
