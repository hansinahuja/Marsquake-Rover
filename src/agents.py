class Source:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.traversed = []
        self.queue = []

class Destination:
    def __init__(self, coordinate, isBidirectional = False):
        self.coordinate = coordinate
        self.traversed = []
        self.queue = []
        self.isBidirectional = isBidirectional