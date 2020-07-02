class Agent():
    def __init__(self, location, _type, isMovingAgent = True):
        self.location = location
        self.type = _type                       # type = source/destination
        self.isMovingAgent = isMovingAgent      # does this agent move?
        self.queue = None 
        self.visited = set()
        self.path = {}
        self.logs = []

    from actions.bfs import bfs
    
    def isValidMove(self, environment, x, y):
        if x<0 or x>=environment.length or y<0 or y>=environment.breadth:
            return False
        cell = environment.grid[x][y]
        if cell.type == 'wall':
            return False
        if cell in self.visited:
            return False
        return True

    