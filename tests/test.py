import json
from resources.addition import *

def test_two_plus_two():
    x = 2
    y = 2
    z = two_plus_two(x, y)
    assert z == 4

