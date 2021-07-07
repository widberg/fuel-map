# fuel-map

Notes and assets related to FUEL's map.

<sup>This repository is a relative of the main [FMTK repository](https://github.com/widberg/fmtk).</sup>

## Notes

```cpp
struct PositionVector // sizeof() = 12
{
    float x;
    float z;
    float y;
};
```
"In Area" coordinate system; up is north.

Part of the map that is not "Out of Area" in freeride.

<pre>
          -Y | -65530.0
             |
             |
             |
-X           | (0, 0)    +X
-------------+-------------
-65530.0     |     +65530.0
             |
             |
             |
          +Y | +65530.0
</pre>

"World" coordinate system; up is north.

Whole map image including transparent border.

<pre>
          -Y | -65536.0
             |
             |
             |
-X           | (0, 0)    +X
-------------+-------------
-65536.0     |     +65536.0
             |
             |
             |
          +Y | +65536.0
</pre>

[fuel_map.webp](https://github.com/widberg/fuel-map/blob/master/fuel_map.webp?raw=true) - uncompressed 8192x8192 pixel map image (~66 MB)

[roads.txt](https://github.com/widberg/fuel-map/blob/master/roads.txt?raw=true) - dump of the road data (~52 MB)

Hubs, Liveries, Races, etc. can be gathered from the game's tsc files.
