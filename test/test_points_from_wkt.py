"""
Testing problem180meridian.points_from_wkt()
"""

from ..modules import points_from_wkt


def check_parsing(wkt):
    points, geometry_type = points_from_wkt(wkt)
    if points is not None:
        print(points)


# Testing point wkt for cross180 - None is expected

def test_point():
    check_parsing('POINT (10 20)') is None

def test_multipoint():
    check_parsing('MULTIPOINT ((10 40), (40 30), (20 20), (30 10))') is None
    check_parsing('MULTIPOINT (10 40, 40 30, 20 20, 30 10)') is None


# Testing non processed wkt types for cross180 - None is expected

def test_circularstring():
    check_parsing('CIRCULARSTRING (1 5, 6 2, 7 3)') is None


# Testing empty wkt for cross180 - None is expected

def test_empty_polygon():
    check_parsing('POLYGON EMPTY') is None


# Testing linear wkt

def test_linestring():
    check_parsing('LINESTRING (10 20, 20 30)') == [[[(10.0, 20.0), (20.0, 30.0)]]]


# Testing polygon wkt

def test_polygon():
    check_parsing('MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))') == [[[(40.0, 40.0), (20.0, 45.0), (45.0, 30.0), (40.0, 40.0)]], [[(20.0, 35.0), (10.0, 30.0), (10.0, 10.0), (30.0, 5.0), (45.0, 20.0), (20.0, 35.0)], [(30.0, 20.0), (20.0, 15.0), (20.0, 25.0), (30.0, 20.0)]]]
