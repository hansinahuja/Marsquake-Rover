class Cell:
    def __init__(self, parent, inQueue, isWall):
        self.parent = parent 
        self.inQueue = inQueue        # bool to check if already pushed in queue or not
        self.isWall = isWall          # bool to check if wall              