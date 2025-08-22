from PIL import Image
import pathlib
import numpy as np
import math

TILE_SIZE = 256

with Image.open("fuel_map.webp") as im:
    MAX_NATIVE_ZOOM = int(math.log(im.width / TILE_SIZE,2))
    for zoom in range(0, MAX_NATIVE_ZOOM + 1):
        new_size = TILE_SIZE * (1 << zoom)
        cur_im = im.resize((new_size, new_size))
        print("processing -> zoom: {}, dim: {}".format(zoom, cur_im.size))
        for x in range(0, int(cur_im.width / TILE_SIZE)):
            path = pathlib.Path("docs/tile/" + str(zoom) + "/" + str(x) + "/")
            path.mkdir(parents=True, exist_ok=True)
            for y in range(0, int(cur_im.height / TILE_SIZE)):
                tile = cur_im.crop((x * TILE_SIZE, y * TILE_SIZE, x * TILE_SIZE + TILE_SIZE, y * TILE_SIZE + TILE_SIZE))
                tile = tile.convert('RGB')
                tile.save("docs/tile/{}/{}/{}.png".format(zoom, x, y), "png", optimize=True)
