# Functions to check coordinate chains and find new coordinates

import numpy as np


__all__ = ['check180', 'cross180']


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

    return (new_lon1, new_lat1), (new_lon2, new_lat2)
