# Functions to extract points from geometry
import re

from osgeo import ogr


__all__ = ['points_from_wkt', 'points_from_geometry']


def float_xy_coordinates(coordinate_string):
    coordinate_list = coordinate_string.strip().split(' ')[:2]
    x = float(coordinate_list[0])
    y = float(coordinate_list[1])
    return x, y


def parse_wkt_chain(wkt_coordinates_chain):
    coordinate_string_list = wkt_coordinates_chain.strip('() ').split(',')
    coordinate_list = [float_xy_coordinates(coordinate) for coordinate in coordinate_string_list]
    return coordinate_list


def parse_wkt_multichain(wkt_multichain):

    brackets = len(re.search(r'\)+$', wkt_multichain).group())

    if brackets == 1:
        return [[parse_wkt_chain(wkt_multichain)]]

    elif brackets == 2:
        chains = wkt_multichain.strip('() ').split('),')
        return [[parse_wkt_chain(chain) for chain in chains]]

    elif brackets == 3:
        chains2 = wkt_multichain.strip('() ').split(')),')
        return [[parse_wkt_chain(chain) for chain in chains.split('),')] for chains in chains2]

    else:
        print('Wrong brackets level:', brackets)


def points_from_wkt(wkt):

    geometry_type = re.search('^[A-Z]+', wkt).group()

    if geometry_type in ('POINT', 'MULTIPOINT'):
        print('No crossing for type:', geometry_type)
        return None

    elif geometry_type not in ('LINESTRING', 'MULTILINESTRING', 'POLYGON', 'MULTIPOLYGON'):
        print('Incorrect geometry type for crossing check:', geometry_type)
        return None

    elif re.search('EMPTY$', geometry_type):
        print('Geometry is empty:', wkt)
        return None

    wkt_multichain_search = re.search(r'\([()\d\., ]+\)', wkt)

    if wkt_multichain_search is None:
        print('Wkt coordinates not found:', wkt)
        return None

    else:
        return parse_wkt_multichain(wkt_multichain_search.group())


def points_from_geometry(geometry):

    assert isinstance(geometry, ogr.Geometry)

    return points_from_wkt(geometry.ExportToWkt())


if __name__ == '__main__':

    def check_parsing(wkt):
        points = points_from_wkt(wkt)
        if points is not None:
            print(points)

    check_parsing('POINT (10 20)')
    check_parsing('CIRCULARSTRING (1 5, 6 2, 7 3)')
    check_parsing('POLYGON EMPTY')
    check_parsing('LINESTRING (10 20, 20 30)')
    check_parsing('MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))')
    check_parsing('MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))')
