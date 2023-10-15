import numpy as np

try:
    from osgeo import ogr
except ImportError:
    import ogr

from .polygonhierarchy import PolygonHierarchy
from .get_coordinates import points_from_geometry
from .check_coordinates import check180, cross180


__all__ = ['split180_coordinates', 'split180_multilinestring',
           'split180_multipolygon', 'split180_geometry']


# Split coordinates by the 180th meridian creating new coordinate chains
def split180_coordinates(coordinates, check, lon_buffer=0):

    assert len(coordinates) - 1 == len(check)

    chains = [[coordinates[0]]]

    for i in range(len(check)):

        if check[i]:
            chains[-1].append(coordinates[i+1])
        else:
            new_coord1, new_coord2 = cross180(
                *tuple(coordinates[i:i + 2]),
                lon_buffer=lon_buffer)
            chains[-1].append(new_coord1)
            chains.append([new_coord2, coordinates[i+1]])

    return chains


# Split linestring/multilinestring geometry by the 180th meridian
def split180_multilinestring(coordinates, lon_buffer=0):

    chains = []

    for poly in coordinates:

        cross, check = check180(coordinates[0])

        if cross:
            chain = split180_coordinates(poly, check, lon_buffer=lon_buffer)
            chains.extend(chain)
        else:
            chains.append(poly)

    wkt = 'MULTILINESTRING ((%s))' % '),('.join(
        [
            ','.join([f"{p[0]} {p[1]}" for p in chain]) for chain in chains
        ]
    )

    multilinestring = ogr.Geometry(wkt=wkt)

    return multilinestring


# Converts coordinate chains into a list of MultiPolygon geometry
def coordinate_chains_to_multipolygon(chains):

    # Chains from split180_coordinates are expected;
    # need to finish all the polygon chains to make correct wkt
    if len(chains) > 1:
        chains[0].extend(chains.pop())
        for chain in chains[1:]:
            chain.append(chain[0])

    wkt_list = [
        'MULTIPOLYGON (((%s)))' %
        ','.join(['%f %f' % (p[0], p[1]) for p in chain]) for chain in chains
    ]

    geom_list = [ogr.Geometry(wkt=wkt) for wkt in wkt_list]
    geoms = PolygonHierarchy(*geom_list)
    multipolygon = geoms.multipolygon()

    return multipolygon


# Split polygon/multipolygon geometry coordinates by the 180th meridian
def split180_multipolygon(coordinates, lon_buffer=0):

    geoms = PolygonHierarchy()

    for polygon in coordinates:

        for chain in polygon:

            cross, check = check180(chain)

            if cross:
                chains = split180_coordinates(chain, check, lon_buffer=lon_buffer)
                multipolygon = coordinate_chains_to_multipolygon(chains)
                geoms.join_geometry(multipolygon)
            else:
                point_str = ','.join(['%f %f' % (p[0], p[1]) for p in chain])
                wkt = f"MULTIPOLYGON ((({point_str})))"
                geoms.join_geometry(ogr.Geometry(wkt=wkt))

    return geoms.multipolygon()


# Split ogr.Geometry by the 180th meridian
def split180_geometry(geometry, lon_buffer=0, filter_valid_polygons=False):

    # Avoid false splitting for topologically correct polygons
    if filter_valid_polygons:
        gtype = geometry.GetGeometryType()
        if geometry.IsValid():
            if gtype == 6:
                return geometry
            elif gtype == 3:
                new_wkt = f'MULTIPOLYGON ({geometry.ExportToWkt()})'
                new_geometry = ogr.CreateGeometryFromWkt(new_wkt)
                return new_geometry

    coordinates, geometry_type = points_from_geometry(geometry)

    if geometry_type is None:
        raise Exception('Geometry type not found')

    elif geometry_type in ('POINT', 'MULTIPOINT'):
        pass

    elif geometry_type in ('LINESTRING', 'MULTILINESTRING'):
        return split180_multilinestring(coordinates, lon_buffer=lon_buffer)

    elif geometry_type in ('POLYGON', 'MULTIPOLYGON'):
        return split180_multipolygon(coordinates, lon_buffer=lon_buffer)

    else:
        raise Warning(f'Unsupported geometry type {geometry_type}')

    return geometry
