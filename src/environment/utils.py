class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = [[x+1, y], 
                            [x-1, y],
                            [x, y+1],
                            [x, y-1]]

class Cell:
    def __init__(self, location, _type = 'free'):
        self.location = location
        self.type = _type       # type = source/destination/free/wall/visited/inQueue
        self.srcAgent = None    # To backtrack for final path
        self.destAgent = None
        

    # To make dictionaries and sets of Cell objects
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            self.location.x == other.location.x and \
            self.location.y == other.location.y

    def __hash__(self):
        return hash(str(self.location.x) + ' ' + str(self.location.y)) 