"""
Testing problem180meridian.split180_geometry()
"""

from osgeo import ogr

from ..problem180meridian import split180_geometry


def check_parsing(feature, **kwargs):
    geometry = feature.GetGeometryRef()
    new_geometry = split180_geometry(geometry, **kwargs)
    if new_geometry is not None:
        print(new_geometry)
    return new_geometry


test_ds = ogr.Open('./test/test_data/test_geometry.geojson')
test_lr = test_ds.GetLayer()


# Testing POINT geometry for cross180 - None is expected

def test_point():
    check_parsing(test_lr.GetFeature(1)) is None


# Testing LINESTRING geometry for cross180 - None is expected

def test_linestring():
    check_parsing(test_lr.GetFeature(0)).ExportToWkt() == 'MULTILINESTRING ((24.5415438402914 13.5588583164334, 25.5100146734532 4.19366085458475,32.6431265127727 6.13284981165079))'


# Testing POLYGON geometry for cross180 - None is expected

def test_polygon():
    check_parsing(test_lr.GetFeature(2)).ExportToWkt() == 'MULTIPOLYGON (((42.2673084292096 59.944926664255, 75.0211577247333 62.6922826805411, 47.1942850696495 67.2099881248319, 23.0620579829856 63.2777691933206, 26.5176224655007 66.1661342312123, 15.0717845363254 58.7370412696996, 42.2673084292096 59.9449266642551)))'


# Testing topologically correct polygons supposed to be splitted

def test_polygon_false_split():
    check_parsing(test_lr.GetFeature(0), filter_valid_polygons=False).ExportToWkt() == \
    'MULYIPOLYGON ((-170 -50, -180 -50, -180 0, -170 0, -170 50)),((170 -50, 170 0, 180 0, 180 -50, 170 -50))'

def test_polygon_abort_split():
    check_parsing(test_lr.GetFeature(0), filter_valid_polygons=True).ExportToWkt() == \
    'MULTIPOLYGON (((-170 -50, 170 -50, 170 0, -170 0, -170 -50)))'
