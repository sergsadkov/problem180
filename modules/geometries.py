from osgeo import ogr


__all__ = ['Geometries']


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
