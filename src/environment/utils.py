class Location:

    """
    Class to wrap location attributes.
    Attributes:
        x: X-coordinate of cell.
        y: Y-coordinate of cell.
        neighbours: List of neighbours of current cell.
    """

    def __init__(self, x, y):

        """
        Constructor for class Location.
        """

        self.x = x
        self.y = y
        self.neighbours = [[x, y+1], [x+1, y+1], [x+1, y],
                           [x+1, y-1], [x, y-1], [x-1, y-1], [x-1, y], [x-1, y+1]]


class Cell:

    """
    Class to represent a cell in the environment.
    Attributes:
        location: Location of the cell.
        type: Type of the cell (source, destination, wall, etc.)
        srcAgent: Source agent which reaches the cell first.
        destAgent: Destination agent which reaches the cell first.
        weight: Cost of travelling to this cell.
    """

    def __init__(self, location, _type='free'):

        """
        Constructor for class Cell.
        """

        self.location = location
        self.type = _type       
        self.srcAgent = None  
        self.destAgent = None
        self.weight = 1

    # Overloaded equality function
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            self.location.x == other.location.x and \
            self.location.y == other.location.y

    # Overloaded comparison function
    def __lt__(self, other):
        return self.weight < other.weight

    # Overloaded hashing function
    def __hash__(self):
        return hash(str(self.location.x) + ' ' + str(self.location.y))
