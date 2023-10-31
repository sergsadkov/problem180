"""
Testing functions from pole_points.py
"""


from ..problem180meridian import check180
from ..problem180meridian.pole_points import find_pole


# Testing find_pole()


def test_no_poles():
    coordinates = [[0, 0], [0, 10], [10, 10], [0, 0]]
    cross, check = check180(coordinates)
    pole_position = find_pole(coordinates, check, north=True)
    assert pole_position is None


def test_north_pole():
    coordinates = [[160, 80], [-100, 80], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    pole_position = find_pole(coordinates, check, north=True)
    assert pole_position == 0


def test_south_pole():
    coordinates = [[160, 80], [-100, 80], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    pole_position = find_pole(coordinates, check, north=False)
    assert pole_position == 0


def test_north_pole_with_crossing():
    coordinates = [[160, 80], [-100, 80], [-100, 60], [160, 50], [-100, 40], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    # print(check)
    pole_position = find_pole(coordinates, check, north=True)
    assert pole_position == 0


def test_south_pole_with_crossing():
    coordinates = [[160, 80], [-100, 80], [-100, 60], [160, 50], [-100, 40], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    pole_position = find_pole(coordinates, check, north=False)
    assert pole_position == 3
