class Wall:
    def __init__(self, coordinate):
        self.coordinate = coordinate

class Traversed:
    def __init__(self, coordinate, parent):
        self.coordinate = coordinate
        self.parent = parent

class InQueue:
    def __init__(self, coordinate, parent):
        self.coordinate = coordinate
        self.parent = parent

class Free:
    def __init__(self, coordinate):
        self.coordinate = coordinate