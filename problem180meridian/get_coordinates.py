# Functions to extract points from geometry
import re

from osgeo import ogr


__all__ = ['points_from_wkt', 'points_from_geometry', 'wkt_close_chain', 'wkt_brackets']


class WktParsingException(Exception):

    def __init__(self, *args, **kwargs):
        pass


def float_xy_coordinates(coordinate_string):
    coordinate_list = coordinate_string.strip().split(' ')[:2]
    x = float(coordinate_list[0])
    y = float(coordinate_list[1])
    return x, y


def parse_wkt_chain(wkt_coordinates_chain):
    coordinate_string_list = wkt_coordinates_chain.strip('() ').split(',')
    coordinate_list = [float_xy_coordinates(coordinate) for coordinate in coordinate_string_list]
    return coordinate_list


def parse_wkt_multichain(wkt_multichain, geom_type):

    if geom_type == 'LINESTRING':
        return [parse_wkt_chain(wkt_multichain)]

    elif geom_type == 'MULTILINESTRING':
        chains = wkt_multichain.strip('() ').split('),')
        return [parse_wkt_chain(chain) for chain in chains]

    elif geom_type == 'POLYGON':
        chains = wkt_multichain.strip('() ').split('),')
        return [[parse_wkt_chain(chain) for chain in chains]]

    elif geom_type == 'MULTIPOLYGON':
        chains2 = wkt_multichain.strip('() ').split(')),')
        return [[parse_wkt_chain(chain) for chain in chains.split('),')] for chains in chains2]

    else:
        raise WktParsingException('Wrong geometry type:', geom_type)


def points_from_wkt(wkt):

    geometry_type = re.search('^[A-Z]+', wkt).group()

    if geometry_type in ('POINT', 'MULTIPOINT'):
        print('No crossing for type:', geometry_type)
        return None, geometry_type

    elif geometry_type not in ('LINESTRING', 'MULTILINESTRING', 'POLYGON', 'MULTIPOLYGON'):
        print('Incorrect geometry type for crossing check:', geometry_type)
        return None, geometry_type

    elif re.search('EMPTY$', geometry_type):
        print('Geometry is empty:', wkt)
        return None, geometry_type

    wkt_multichain_search = re.search(r'\([()\-\d\., ]+\)', wkt)

    if wkt_multichain_search is None:
        print('Wkt coordinates not found:', wkt)
        return None, geometry_type

    else:
        coordinates = parse_wkt_multichain(wkt_multichain_search.group(), geometry_type)
        return coordinates, geometry_type


def wkt_close_chain(geometry_type):
    if geometry_type in ('LINESTRING', 'MULTILINESTRING'):
        return False
    elif geometry_type in ('POLYGON', 'MULTIPOLYGON'):
        return True
    else:
        raise WktParsingException(f'Incorrect geometry type: {geometry_type}')


def wkt_brackets(geometry_type):
    if geometry_type in ['LINESTRING']:
        return 1
    elif geometry_type in ['POLYGON', 'MULTILINESTRING']:
        return 2
    elif geometry_type in ['MULTIPOLYGON']:
        return 3
    else:
        raise WktParsingException(f'Incorrect geometry type: {geometry_type}')


def points_from_geometry(geometry):

    assert isinstance(geometry, ogr.Geometry)

    return points_from_wkt(geometry.ExportToWkt())


if __name__ == '__main__':

    def check_parsing(wkt):
        points, geometry_type = points_from_wkt(wkt)
        if points is not None:
            print(points)

    check_parsing('POINT (10 20)')
    check_parsing('CIRCULARSTRING (1 5, 6 2, 7 3)')
    check_parsing('POLYGON EMPTY')
    check_parsing('LINESTRING (10 20, 20 30)')
    check_parsing('MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))')
    check_parsing('MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))')
