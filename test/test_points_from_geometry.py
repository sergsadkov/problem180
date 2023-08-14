"""
Testing problem180meridian.points_from_wkt()
"""

from osgeo import ogr

from problem180meridian import points_from_geometry


def check_parsing(feature):
    geometry = feature.GetGeometryRef()
    points = points_from_geometry(geometry)
    if points is not None:
        print(points)


test_ds = ogr.Open('./test/test_data/test_geometry.geojson')
test_lr = test_ds.GetLayer()


# Testing POINT geometry for cross180 - None is expected

def test_point():
    check_parsing(test_lr.GetFeature(1)) is None


# Testing LINESTRING geometry for cross180 - None is expected

def test_linestring():
    check_parsing(test_lr.GetFeature(0)) == [[[(24.5415438402914, 13.5588583164334), (25.5100146734532, 4.19366085458475),(32.6431265127727, 6.13284981165079)]]]


# Testing POLYGON geometry for cross180 - None is expected

def test_polygon():
    check_parsing(test_lr.GetFeature(2)) == [[[(42.2673084292096, 59.944926664255), (75.0211577247333, 62.6922826805411), (47.1942850696495, 67.2099881248319), (23.0620579829856, 63.2777691933206), (26.5176224655007, 66.1661342312123), (15.0717845363254, 58.7370412696996), (42.2673084292096, 59.9449266642551)]]]
