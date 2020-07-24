class Agent():

    """
    Class to represent an agent on the grid.
    Attributes:
        location: Location of the agent
        type: Type of the agent (source/destination)
        isMovingAgent: Whether the agent can move on the grid
        waitList: Current cells in line for exploration.
        visited: Cells already visited.
        path: Path through which a cell was reached.
        logs: Changes registered in the last iteration.
        distances: Minimum distances to reach different cells.
    Methods:
        isValidMove: To check if a particular movement is valid.
        breadthFirstSearch, depthFirstSearch, dijkstra, uniformCostSearch: uninformed search algorithms
        aStar, beamSearch, bestFirstSearch, dynamicAStar, idaStar, jumpPointSearch, staticAStar: informed search algorithms
    """


    def __init__(self, location, _type, isMovingAgent=True):

        """
        Constructor for class Agent.
        Arguments:
            location: Location of the agent
            _type: Type of the agent (source/destination)
            isMovingAgent: Whether the agent can move on the grid
        """

        self.location = location
        self.type = _type                      
        self.isMovingAgent = isMovingAgent  
        self.waitList = None
        self.visited = set()
        self.path = {}
        self.logs = []
        self.distances = {}
        

    def isValidMove(self, environment, currentCell, x2, y2, checkVisited = True):

        """
        To check if a particular movement is valid.
        Arguments:
            environment: Environment on which move is to be checked.
            currentCell: Current cell occupied
            x2: X-coordinate of desired move.
            y2: Y-coordinate of desired move.
            checkVisited: Whether visited cell can be visited again.
        Returns:
            If move is valid, return True. Else, return False.
        """

        x1, y1 = currentCell.location.x, currentCell.location.y

        # Check if within bounds
        if x2 < 0 or x2 >= environment.length or y2 < 0 or y2 >= environment.breadth:
            return False

        # Check if cell is a wall
        nextCell = environment.grid[x2][y2]
        if nextCell.type == 'wall':
            return False

        # Check if cell is already visited
        if checkVisited and nextCell in self.visited:
            return False

        # Check for diagonal movement and corner cutting
        manhattanDistance = abs(x1-x2) + abs(y1-y2)
        if manhattanDistance == 2:
            if not environment.allowDiagonals:
                return False
            if not environment.cutCorners:
                if environment.grid[x1][y2].type == 'wall' or environment.grid[x2][y1].type == 'wall':
                    return False
            else:
                if environment.grid[x1][y2].type == 'wall' and environment.grid[x2][y1].type == 'wall':
                    return False

        return True

    # Import all search algorithms
    from actions import (
        aStar,
        beamSearch, 
        bestFirstSearch, 
        breadthFirstSearch, 
        depthFirstSearch, 
        dijkstra, 
        dynamicAStar,
        idaStar,
        jumpPointSearch,
        staticAStar,
        uniformCostSearch
    )
