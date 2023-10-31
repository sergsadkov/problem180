"""
Testing functions from pole_points.py
"""


from ..problem180meridian import check180
from ..problem180meridian.pole_points import update_pole_coordinates


# Testing update_pole_coordinates()


def test_no_poles():
    coordinates = [[0, 0], [0, 10], [10, 10], [0, 0]]
    cross, check = check180(coordinates)
    new_coordinates, new_check = update_pole_coordinates(
        coordinates, check, lon_buffer=0, north=False, south=False)
    assert new_coordinates == coordinates


def test_north_pole():
    coordinates = [[160, 80], [-100, 80], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    new_coordinates, new_check = update_pole_coordinates(
        coordinates, check, lon_buffer=0, north=True, south=False)
    assert new_coordinates == [(180, 80.0), (180.0, 90.0), (-180.0, 90.0), (-180, 80.0), [160, 80], [-100, 80], [40, 80], [160, 80]]


def test_south_pole():
    coordinates = [[160, 80], [-100, 80], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    new_coordinates, new_check = update_pole_coordinates(
        coordinates, check, lon_buffer=0, north=False, south=True)
    assert new_coordinates == [(180, 80.0), (180.0, -90.0), (-180.0, -90.0), (-180, 80.0), [160, 80], [-100, 80], [40, 80], [160, 80]]


def test_north_pole_with_crossing():
    coordinates = [[160, 80], [-100, 80], [-100, 60], [160, 50], [-100, 40], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    new_coordinates, new_check = update_pole_coordinates(
        coordinates, check, lon_buffer=0, north=True, south=False)
    print(new_coordinates)
    print(new_check)
    assert new_coordinates == [(180, 80.0), (180.0, 90.0), (-180.0, 90.0), (-180, 80.0), [160, 80], [-100, 80], [-100, 60], [160, 50], [-100, 40], [40, 80], [160, 80]]


def test_south_pole_with_crossing():
    coordinates = [[160, 80], [-100, 80], [-100, 60], [160, 50], [-100, 40], [40, 80], [160, 80]]
    cross, check = check180(coordinates)
    new_coordinates, new_check = update_pole_coordinates(
        coordinates, check, lon_buffer=0, north=False, south=True)
    print(new_coordinates)
    print(new_check)
    assert new_coordinates == [[160, 80], [-100, 80], [-100, 60], (180, 48.0), (180.0, -90.0), (-180.0, -90.0), (-180, 48.0), [160, 50], [-100, 40], [40, 80], [160, 80]]
