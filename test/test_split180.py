"""
Testing problem180meridian.split180()
"""

from problem180meridian import split180_multipolygon


# Testing integer coordinates without crossing 180th meridian
def test_split180_int_nochange():

    test_coordinates = [((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)), ((100, 100), (100, 110), (110, 110), (110, 100), (100, 100))]
    output = 'MULTIPOLYGON (((0 0,0 10,10 10,10 0,0 0)),((100 100,100 110,110 110,110 100,100 100)))'

    test_output = split180_multipolygon(test_coordinates).ExportToWkt()
    print(test_output)
    assert output == test_output


# Testing float coordinates without crossing 180th meridian
def test_split180_float_nochange():

    test_coordinates = [((124.055513, -50.114067), (52.829571, -67.533366), (-92.538693, -70.016703), (-169.745357, -51.297079), (124.055513, -50.114067))]
    output = 'MULTIPOLYGON (((124.055513 -50.114067,52.829571 -67.533366,-92.538693 -70.016703,-169.745357 -51.297079,-180 -51.113823,180.0 -51.113823,124.055513 -50.114067)))'

    test_output = split180_multipolygon(test_coordinates).ExportToWkt()
    print(test_output)
    assert output == test_output
