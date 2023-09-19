# problem180meridian
Python module to fix 180 degree crossing issue for vector geodata

## Take care of topology errors on the 180th meridian

Having vector geodata with lines/polygons crossing 180th meridian, their geometry is likely to be displayed wrongly in geographic CRS like EPSG:4326. This module helps to modify the original Linestring, Multilinestring, Polygon, or Multipolygon geometry to be correctly represented in a geographic CRS.

## Install

The module is available from PyPi, one may install it using pip:

`pip install problem180meridian`

To use it from Python console one may use:

`import problem180meridian`

## Usage
The module contains the following functions (version 0.1.4):

`check180(coordinates)` - checks if any segment in a pair of coordinates crosses 180th meridian and returns a tuple of two values. The first one is False if no crossing was found, and True if at least one was found. Without any crossing, the second value is None, otherwise it's an array of bool values where True marks the 180th meridian crossing and False means no crossing.

`cross180(coord1, coord2, lon_buffer=0)` - takes a pair of point coordinates a line between which is supposed to cross the 180th meridian and returns a pair of point coordinates on the crossing between this line and the meridian, or at a distance from it equal to lon_buffer parameter (in longitude degrees).

`split180_coordinates(coordinates, check, lon_buffer=0)` - splits coordinates in a list by the 180th meridian creating new coordinate chains and returns another list with new point coordinates

`split180_multilinestring(coordinates, lon_buffer=0)` - splits linestring/multilinestring geometry coordinates by the 180th meridian and returns ogr.Geometry Multilinestring

`split180_multipolygon(coordinates, lon_buffer=0)` - splits polygon/multipolygon geometry coordinates by the 180th meridian and returns ogr.Geometry Multipolygon

`split180_geometry(geometry, lon_buffer=0)` - splits ogr.Geometry by the 180th meridian and returns another ogr.Geometry. Supported geometry types: Linestring, Multilinestring, Polygon, Multipolygon. Point and Multipoint objects wouldn't be changed; other types cause Warning Exception

## Development

Plans for the module development:

- pole points processing
- backward algorithm to unite geometry separated by the 180th meridian for correct representation in projected CRS, like UTM
- reprojection function to reproject geometry and check 180th meridian crossing, if necessary
- further testing functions to check different geometry shapes, coordinate formats, and complex geometries

## Author

Made by Sergei Sadkov (@sergsadkov)
