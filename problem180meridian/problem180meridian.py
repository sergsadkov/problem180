import numpy as np

try:
    from osgeo import ogr
except ImportError:
    import ogr


__all__ = [
    'Geometries', 'check180', 'cross180', 'split180', 'split180_multipolygon'
]


class GeometriesError(Exception):

    def __init__(self, *args, **kwargs):
        pass


# Arranges a set of polygons to find out which of them are within others
# If any of them is within others they are cut off while creating a new
# multipolygon
class Geometries:

    def __init__(self, *geom_tuple, main_geom=None, level=0):

        assert (main_geom is None) or isinstance(main_geom, ogr.Geometry)

        self.main_geometry = main_geom
        self.level = level
        self.geometries = []

        for geometry in geom_tuple:
            self.join_geometry(geometry)

    def __str__(self):

        if self.main_geometry is None:
            main_wkt = 'No main geometry'
        else:
            main_wkt = self.main_geometry.ExportToWkt()

        tab = '\n\t' + self.level*'\t'

        return tab.join([main_wkt] + [str(h) for h in self.geometries])

    def check_main_geometry(self, geometry):

        if self.main_geometry is not None:

            if geometry.Within(self.main_geometry):
                # print('Geometry within')
                return 0

            elif self.main_geometry.Within(geometry):
                # print('Hierarchy within')
                return 2

            elif geometry.Intersects(self.main_geometry):
                raise GeometriesError('Unexpected intersection')

            else:
                # print('Out of main geometry')
                return 1

    def join_geometry(self, geometry):

        assert isinstance(geometry, ogr.Geometry)

        main_geometry_check = self.check_main_geometry(geometry)

        if main_geometry_check:
            return main_geometry_check

        new_geoms = Geometries(main_geom=geometry, level=self.level + 1)
        separate = True

        for i in range(len(self.geometries)-1, -1, -1):

            self_geoms = self.geometries[i]
            separate = self.geometries[i].join_geometry(geometry)

            if separate == 0:
                # print('Joined hierarchy')
                return 0

            elif separate == 2:
                # Doesn't check if there are intersections within new_geoms
                # Need to fix if used for other polygons but raster footprints!
                new_geoms.geometries.append(self.geometries.pop(i))

            elif geometry.Intersects(self_geoms.main_geometry):
                raise GeometriesError('Unexpected intersection')

        if separate:
            self.geometries.append(new_geoms)
            return 0

        raise GeometriesError('Geometry not processed')

    def multipolygon(self):

        if self.main_geometry is not None:
            multipolygon = self.main_geometry
            for geoms in self.geometries:
                multipolygon = multipolygon.Difference(geoms.multipolygon())

        elif len(self.geometries) != 0:
            multipolygon = self.geometries[0].multipolygon()
            for geoms in self.geometries[1:]:
                multipolygon = multipolygon.Union(geoms.multipolygon())

        else:
            multipolygon = ogr.Geometry(6)

        return multipolygon


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


# Split polygon geometry by the 180th meridian creating a multipolygon
def split180(coordinates, check, lon_buffer=0):

    assert len(coordinates) - 1 == len(check)
    assert coordinates[0] == coordinates[-1]
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

    # need to finish all the polygon chains to make correct wkt
    if len(chains) > 1:
        chains[0].extend(chains.pop())
        for chain in chains[1:]:
            chain.append(chain[0])

    wkt_list = ['MULTIPOLYGON (((%s)))' % ','.join(['%f %f' %
                (p[0], p[1]) for p in chain]) for chain in chains]

    polygons = [ogr.Geometry(wkt=wkt) for wkt in wkt_list]
    geoms = Geometries(*polygons)
    multipolygon = geoms.multipolygon()

    return multipolygon


# Split polygon/multipolygon geometry by the 180th meridian
def split180_multipolygon(coordinates, lon_buffer=0):

    geoms = Geometries()

    for poly in coordinates:

        cross, check = check180(coordinates[0])

        if cross:
            geoms.join_geometry(split180(poly, check, lon_buffer=lon_buffer))
        else:
            point_str = ','.join(['%f %f' % (p[0], p[1]) for p in poly])
            wkt = f"MULTIPOLYGON ((({point_str})))"
            geoms.join_geometry(ogr.Geometry(wkt=wkt))

    return geoms.multipolygon()
