class Agent():
    def __init__(self, location, _type, isMovingAgent=True):
        self.location = location
        self.type = _type                       # type = source/destination
        self.isMovingAgent = isMovingAgent      # does this agent move?
        self.waitList = None
        self.visited = set()
        self.path = {}
        self.logs = []
        self.distances = {}

    from actions.breadthFirstSearch import breadthFirstSearch
    from actions.depthFirstSearch import depthFirstSearch
    from actions.dijkstra import dijkstra
    from actions.bestFirstSearch import bestFirstSearch
    from actions.aStar import aStar
    from actions.idaStar import idaStar
    from actions.beamSearch import beamSearch
    from actions.jumpPointSearch import jumpPointSearch
    from actions.ida import ida

    def isValidMove(self, environment, currentCell, x2, y2, checkVisited = True):
        x1, y1 = currentCell.location.x, currentCell.location.y
        if x2 < 0 or x2 >= environment.length or y2 < 0 or y2 >= environment.breadth:
            return False
        nextCell = environment.grid[x2][y2]
        if nextCell.type == 'wall':
            return False
        if checkVisited and nextCell in self.visited:
            return False
        manhattanDistance = abs(x1-x2) + abs(y1-y2)
        if manhattanDistance == 2:
            if not environment.allowDiagonals:
                return False
            if not environment.cutCorners:
                if environment.grid[x1][y2].type == 'wall' or environment.grid[x2][y1].type == 'wall':
                    return False
        return True
