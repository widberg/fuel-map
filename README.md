# fuel-map

Notes and assets related to FUEL's map.

<sup>This repository is a relative of the main [FMTK repository](https://github.com/widberg/fmtk).</sup>

## Notes

While some in-game development menus will swap the names of the y and z components, the data is stored in the order of the `Vec3f` struct bellow assuming +Y is up, +X is east, and +Z is south. See the [fmtk wiki Coordinate Systems entry](https://github.com/widberg/fmtk/wiki/Coordinate-Systems) for more information.

```cpp
struct Vec3f
{
    float x;
    float y;
    float z;
};
```

"In Area" coordinate system; -Z is north.

Part of the map that is not "Out of Area" in freeride. `Alpha = 1`.

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

"World" coordinate system; -Z is north.

Whole map image excluding transparent border. `0 < Alpha < 1`.

<pre>
          -Z | -65537.0
             |
             |
             |
-X           | (0, 0)    +X
-------------+-------------
-65537.0     |     +65535.0
             |
             |
             |
          +Z | +65535.0
</pre>

[fuel_map.webp](https://github.com/widberg/fuel-map/blob/master/fuel_map.webp?raw=true) - uncompressed 8192x8192 pixel map image (~66 MB)

[roads.txt](https://github.com/widberg/fuel-map/blob/master/roads.txt?raw=true) - dump of the road data (~52 MB)

[binary_maps](https://github.com/widberg/fuel-map/blob/master/docs/binary_maps) - visualizations of the height and terrain type maps

Hubs, Liveries, Races, etc. can be gathered from the game's tsc files.
