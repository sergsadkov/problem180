"""
Testing problem180meridian.cross180()
"""

from problem180meridian import cross180


# Test cross180() for integer coordinates upper and below zero and
# distance_from_180lon=0.0
def test_cross180_int():

    test_coordinates = [
        ([(175, 0), (-175, 0)], {}, ((180.0, 0.0), (-180.0, 0.0))),
        ([(175, 10), (-175, 20)], {}, ((180.0, 15.0), (-180.0, 15.0))),
        ([(175, -10), (-175, -20)], {}, ((180.0, -15.0), (-180.0, -15.0))),
        ([(175, 5), (-175, -5)], {}, ((180.0, -0.0), (-180.0, 0.0))),
        ([(-175, 0), (175, 0)], {}, ((-180.0, 0.0), (180.0, 0.0))),
        ([(-175, 10), (175, 20)], {}, ((-180.0, 15.0), (180.0, 15.0))),
        ([(-175, 5), (175, -5)], {}, ((-180.0, 0.0), (180.0, 0.0))),
    ]

    for args, kwargs, output in test_coordinates:
        test_output = cross180(*args, **kwargs)
        print(args, test_output)
        assert output == test_output


# Test cross180() for integer coordinates upper and below zero and
# distance_from_180lon=1.0
def test_cross180_int_dist1deg():

    test_coordinates = [
        ([(175, 0), (-175, 0)], {'distance_from_180lon': 1.0}, ((179.0, 0.0), (-179.0, 0.0))),
        ([(175, 10), (-175, 20)], {'distance_from_180lon': 1.0}, ((179.0, 14.0), (-179.0, 16.0))),
        ([(175, -10), (-175, -20)], {'distance_from_180lon': 1.0}, ((179.0, -14.0), (-179.0, -16.0))),
        ([(175, 5), (-175, -5)], {'distance_from_180lon': 1.0}, ((179.0, 1.0), (-179.0, -1.0))),
        ([(-175, 0), (175, 0)], {'distance_from_180lon': 1.0}, ((-179.0, 0.0), (179.0, 0.0))),
        ([(-175, 10), (175, 20)], {'distance_from_180lon': 1.0}, ((-179.0, 14.0), (179.0, 16.0))),
        ([(-175, 5), (175, -5)], {'distance_from_180lon': 1.0}, ((-179.0, 1.0), (179.0, -1.0))),
    ]

    for args, kwargs, output in test_coordinates:
        test_output = cross180(*args, **kwargs)
        print(args, test_output)
        assert output == test_output
