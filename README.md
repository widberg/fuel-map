# fuel-map

Notes and assets related to FUEL's map.

<sup>This repository is a relative of the main [FMTK repository](https://github.com/widberg/fmtk).</sup>

## Getting Started

View the map online at https://widberg.me/fuel-map/

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

Past the +/-70000.0 point the height and biome maps become mirrored and continue, until you hit the end of the mirror world and it mirrors again, forever, or until your computer melts. I presume the reason it mirrors instead of wrapping is to prevent sharp changes in terrain at the edges, even though the game would kill you long before you make it that far. A simple Python function that converts actual positions along an axis to the corresponding position in the real world, accounting for the repeated mirroring:

```python
def mirrored_position(n: float) -> float:
    return -70000 + 140000 - abs(((n + 70000) % 280000) - 140000)
```

At this point it should be obvious that this coordinate system maps actual positions to real world positions via a triangle wave of amplitude 70,000 and period 280,000, shifted so that it oscillates between –70,000 and +70,000.

Due to floating point precision decreasing as your actual position becomes very high along an axis, the world becomes less detailed along that axis as it sampled the same points in the height map for what would have been multiple distinct coordinates in a mirror world closer to the real world. This actually happens much faster than I would have expected so the game must be multiplying the position values at some point and pushing them out of range. I saw significant stair-stepping in mountains along the Z axis at -421,682.9 when I wouldn't have expected to see it until past 2<sup>24</sup> which is the point at which only every other integer is representable by a float. Now I have to recommend [pannenkoek2012's video about pendulums in SM64](https://www.youtube.com/watch?v=nYDmBdUalgo).

Also, since things like WorldRef_Z, GwRoads_Z, and bodies of water all use actual positions you won't find them in the other worlds. And remember that this is just an artifact of how the game samples the height and biome maps, it isn't actually mirroring the coordinate systems, models appear correctly and north is still in the negative Z direction.

[fuel_map.webp](https://github.com/widberg/fuel-map/blob/master/fuel_map.webp?raw=true) - uncompressed 8192x8192 pixel map image (~66 MB)

[binary_maps](https://github.com/widberg/fuel-map/blob/master/docs/binary_maps) - visualizations of the height and terrain type maps

[geogen.py](https://github.com/widberg/fuel-map/blob/master/geogen.py) - script to gather hubs, liveries, races, etc. from the game's tsc, DPC, and exe files into GeoJSON files.
