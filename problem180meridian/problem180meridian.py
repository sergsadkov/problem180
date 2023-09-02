import numpy as np

try:
    from osgeo import ogr
except ImportError:
    import ogr

from ..modules import Geometries, points_from_geometry


__all__ = ['check180', 'cross180', 'split180_coordinates',
           'split180_multipolygon', 'split180_multilinestring',
           'split180_geometry']


# Returns True if value is positive or zero and False if it is negative
def array_not_negative(array):
    return np.sign(np.sign(array) + 1).astype(bool)


# Checks if any segment in a pair of coordinates crosses 180th meridian
# It's considered so if abs(x2 - x1) > abs(x2_1 - x1_1) where
# xi_1 = xi + (xi < 0) * 360
# If any crossing is found a check_array is returned where crossing pairs
# are marked as True
def check180(coordinates):

    longitudes = np.array([p[0] for p in coordinates])
    signs = array_not_negative(longitudes)

    if list(np.unique(signs)) == [0, 1]:
        distances = abs(longitudes[1:] - longitudes[:-1])
        longitudes_fixed = longitudes + ((signs == 0) * 360)
        distances_fixed = abs(longitudes_fixed[1:] - longitudes_fixed[:-1])
        # Need to add small value below to avoid Python calculation errors
        check_array = array_not_negative(distances_fixed - distances + 0.000001)
        return True, check_array
    else:
        return False, None


# Create coordinates for two points in a segment crossing 180th meridian
# Setting lon_buffer one can separate them from each other and
# the meridian itself
def cross180(coord1, coord2, lon_buffer=0):

    if coord1[0] > 0:
        assert coord2[0] < 0
        img_lon2 = coord2[0] + 360
        new_lon1 = 180 - abs(lon_buffer)
    else:
        assert coord2[0] >= 0
        img_lon2 = coord2[0] - 360
        new_lon1 = abs(lon_buffer) - 180

    if (img_lon2 - coord1[0]) == 0:
        angle_coefficient = 1
    else:
        angle_coefficient = (coord2[1] - coord1[1]) / (img_lon2 - coord1[0])

    new_lon2 = (-1) * new_lon1
    new_lat1 = coord1[1] + angle_coefficient * (new_lon1 - coord1[0])
    new_lat2 = coord2[1] + angle_coefficient * (new_lon2 - coord2[0])

    return (new_lon1, new_lat1), (- new_lon1, new_lat2)


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
    geoms = Geometries(*geom_list)
    multipolygon = geoms.multipolygon()

    return multipolygon


# Split polygon/multipolygon geometry coordinates by the 180th meridian
def split180_multipolygon(coordinates, lon_buffer=0):

    geoms = Geometries()

    for polygon in coordinates:
        for arring in polygon:

            cross, check = check180(arring)

            if cross:
                chains = split180_coordinates(arring, check, lon_buffer=lon_buffer)
                multipolygon = coordinate_chains_to_multipolygon(chains)
                geoms.join_geometry(multipolygon)
            else:
                point_str = ','.join(['%f %f' % (p[0], p[1]) for p in arring])
                wkt = f"MULTIPOLYGON ((({point_str})))"
                geoms.join_geometry(ogr.Geometry(wkt=wkt))

    return geoms.multipolygon()


# Split ogr.Geometry by the 180th meridian
def split180_geometry(geometry, lon_buffer=0):

    coordinates, geometry_type = points_from_geometry(geometry)

    if geometry_type is None:
        print('Geometry type not found')
        return None

    elif geometry_type in ('POINT', 'MULTIPOINT'):
        return geometry

    elif geometry_type in ('LINESTRING', 'MULTILINESTRING'):
        return split180_multilinestring(coordinates, lon_buffer=lon_buffer)

    elif geometry_type in ('POLYGON', 'MULTIPOLYGON'):
        return split180_multipolygon(coordinates, lon_buffer=lon_buffer)

    else:
        print('Unsupported geometry type', geometry_type)
        return None
