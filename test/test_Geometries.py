"""
Testing problem180meridian.geometries
"""

from problem180meridian import Geometries

from osgeo import ogr


# Testing unification 4 geometries with int coordinates,
# 1 of them is within the other one,
# and 1 more os within with 1 line touching its border
def test_geometries_int_1within_1touch():

    test_geometries = [
        ogr.Geometry(wkt='MULTIPOLYGON (((20 20, 20 21, 21 21, 21 20, 20 20)))'),
        ogr.Geometry(wkt='MULTIPOLYGON (((10 10, 10 11, 11 11, 11 10, 10 10)))'),
        ogr.Geometry(wkt='MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))'),
        ogr.Geometry(wkt='MULTIPOLYGON (((0 0, 0 100, 100 100, 100 0, 0 0)))'),
    ]

    hierarchy = Geometries(*test_geometries)
    output = hierarchy.multipolygon().ExportToWkt()

    assert output == 'POLYGON ((100 0,1 0,1 1,0 1,0 100,100 100,100 0),(11 11,10 11,10 10,11 10,11 11),(21 20,21 21,20 21,20 20,21 20))'
