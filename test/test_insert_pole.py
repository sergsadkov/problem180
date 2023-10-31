"""
Testing functions from pole_points.py
"""


from ..problem180meridian.pole_points import insert_pole


# Testing insert_pole()


def test_north_pole():
    coordinates = [[160, 80], [-100, 80], [40, 80], [160, 80]]
    new_coordinates = insert_pole(coordinates, 0, north=True, lon_buffer=0)
    assert new_coordinates == [(180, 80.0), (180.0, 90.0), (-180.0, 90.0), (-180, 80.0), [160, 80], [-100, 80], [40, 80], [160, 80]]


def test_south_pole():
    coordinates = [[160, 80], [-100, 80], [40, 80], [160, 80]]
    new_coordinates = insert_pole(coordinates, 0, north=False, lon_buffer=0)
    assert new_coordinates == [(180, 80.0), (180.0, -90.0), (-180.0, -90.0), (-180, 80.0), [160, 80], [-100, 80], [40, 80], [160, 80]]
