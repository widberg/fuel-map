# fuel-map

Notes and assets related to FUEL's map.

<sup>This repository is a relative of the main [FMTK repository](https://github.com/widberg/fmtk).</sup>

## Notes

See also: [FMTK Map wiki entry](https://github.com/widberg/fmtk/wiki/Map).

While some in-game development menus will swap the names of the y and z components, the data is stored in the order of the `Vec3f` struct bellow assuming +Y is up, +X is east, and +Z is south. See the [fmtk wiki Coordinate Systems entry](https://github.com/widberg/fmtk/wiki/Coordinate-Systems) for more information.

```cpp
struct Vec3f
{
    float x;
    float y;
    float z;
};
```

The units used in game, and in this project, are "Zouna units". One Zouna unit (`zu`) is equal to one meter (`m`) in FUEL. Everything is represented as `zu`s/`m`s internally and converted to miles and kilometers when needed. Also, speeds are usually represented in terms of seconds and converted to be in terms of hours when needed. More examples of engine defined units can be found on the [Valve Software Developer Community Wiki Unit page](https://developer.valvesoftware.com/wiki/Unit).

-Z is north.

Part of the map that is not "Out of Area" in freeride.

<pre>
          -Z | -65530.0
             |
             |
             |
-X           | (0, 0)    +X
-------------+-------------
-65530.0     |     +65530.0
             |
             |
             |
          +Z | +65530.0
</pre>

Whole `fuel_map.webp` image including "Out of Area".

<pre>
          -Z | -70000.0
             |
             |
             |
-X           | (0, 0)    +X
-------------+-------------
-70000.0     |     +70000.0
             |
             |
             |
          +Z | +70000.0
</pre>

[fuel_map.webp](https://github.com/widberg/fuel-map/blob/master/fuel_map.webp?raw=true) - uncompressed 8192x8192 pixel map image (~66 MB)

[binary_maps](https://github.com/widberg/fuel-map/blob/master/docs/binary_maps) - visualizations of the height and terrain type maps

[geogen.py](https://github.com/widberg/fuel-map/blob/master/geogen.py) - script to gather hubs, liveries, races, etc. from the game's tsc, DPC, and exe files into GeoJSON files.
