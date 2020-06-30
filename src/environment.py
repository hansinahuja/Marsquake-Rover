from utilities import Coordinate

class Cell:
    def __init__(self, coordinate, parent = None, isWall = False, inQueue = False, isTraversed = False):
        self.coordinate = coordinate
        self.parent = parent 
        self.isWall = isWall            # bool to check if wall  
        self.inQueue = inQueue          # bool to check if already pushed in queue or not
        self.isTraversed = isTraversed

class Environment:
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth
        self.grid = [ [Cell(Coordinate(x, y)) for x in range(breadth)] for y in range(length) ]