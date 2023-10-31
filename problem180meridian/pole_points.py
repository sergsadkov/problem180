# Functions to show polygon/multipolygon geometries containing pole points


from osgeo import ogr, osr

from .check_coordinates import cross180


# __all__ = []


NORTH_POLE = ogr.CreateGeometryFromWkt('POINT (0 90)')
SOUTH_POLE = ogr.CreateGeometryFromWkt('POINT (0 -90)')
SRS4326 = osr.SpatialReference()
SRS4326.ImportFromEPSG(4326)

# Check if a polygon from coordinates chain contains pole points
def pole_within(coordinates, srs=None):

    wkt_coordinates = ','.join([f'{p[0]} {p[1]}' for p in coordinates])
    wkt = f'POLYGON (({wkt_coordinates}))'
    polygon = ogr.CreateGeometryFromWkt(wkt)

    if srs is not None:
        if not srs.IsSame(SRS4326):
            transform = osr.CoordinateTransformation(SRS4326, srs)

    north = NORTH_POLE.Within(polygon)
    south = SOUTH_POLE.Within(polygon)

    return north, south


# Find where is the line to insert pole coordinates in a coordinate chain
def find_pole(coordinates, check, north=True):

    if check is not None: # like if no crossing found by split180()

        assert len(coordinates) - 1 == len(check)

        clat = []

        for i in range(len(check)):
            if not check[i]:
                clat.append([coordinates[i][1], i])

        clat.sort()
        # print(clat)
        if len(clat) > 0:
            if north:
                return clat[-1][1]
            else:
                return clat[0][1]

    return None


# Insert pole points into the coordinate chain
def insert_pole(coordinates, pole_position, north=True, lon_buffer=0):

    # Get new point coordinates
    new_coord1, new_coord2 = cross180(
        *tuple(coordinates[pole_position:pole_position + 2]),
        lon_buffer=lon_buffer)

    # The North Pole latitude is 90; the South Pole latitude is -90
    pole_lat = 180 * (float(north) - 0.5)
    # The longitudes depend on the 180th meridian crossing direction
    lon_sign = 2 * (float(new_coord1[0] > new_coord2[0]) - 0.5)

    pole1 = ((180 - lon_buffer) * lon_sign, pole_lat)
    pole2 = ((lon_buffer - 180) * lon_sign, pole_lat)

    # Insert new points
    for i, point in enumerate([new_coord1, pole1, pole2, new_coord2]):
        coordinates.insert(pole_position + i, point)

    return coordinates


# Update coordinates and check inserting pole points
def update_pole_coordinates(coordinates, check, lon_buffer=0,
                            north=False, south=False):

    if not any([north, south]) or (check is None):
        return coordinates, check

    assert len(coordinates) - 1 == len(check)

    # north, south = pole_within(coordinates)

    if north:
        north_pole_position = find_pole(coordinates, check, north=True)
        coordinates = insert_pole(coordinates, north_pole_position,
                                  lon_buffer=lon_buffer, north=True)
        check[north_pole_position] = False

    if south:
        south_pole_position = find_pole(coordinates, check, north=False)
        coordinates = insert_pole(coordinates, south_pole_position,
                                  lon_buffer=lon_buffer, north=False)
        check[south_pole_position] = False

    return coordinates, check
