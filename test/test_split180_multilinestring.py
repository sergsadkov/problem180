"""
Testing problem180meridian.split180_multilinestring()
"""

from ..problem180meridian import split180_multilinestring


# Testing integer coordinates without crossing 180th meridian
def test_split180_int_nochange():

    test_coordinates = [((0, 0), (0, 10), (10, 10), (10, 0)), ((100, 100), (100, 110), (110, 110), (110, 100))]
    output = 'MULTILINESTRING ((0 0,0 10,10 10,10 0),(100 100,100 110,110 110,110 100))'

    test_output = split180_multilinestring(test_coordinates).ExportToWkt()
    print(test_output)
    assert output == test_output


# Testing float coordinates without crossing 180th meridian
def test_split180_float_nochange():

    test_coordinates = [((160.27414, 66.38205), (165.87357, 65.61501), (160.50426, 58.94171), (166.21875, 62.08660))]
    output = 'MULTILINESTRING ((160.27414 66.38205,165.87357 65.61501,160.50426 58.94171,166.21875 62.0866))'

    test_output = split180_multilinestring(test_coordinates).ExportToWkt()
    print(test_output)
    assert output == test_output
