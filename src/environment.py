from utilities import Coordinate
from cellstates import Free

class Environment:
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth
        self.grid = [ [Free(Coordinate(x, y)) for x in range(length)] for y in range(breadth) ]