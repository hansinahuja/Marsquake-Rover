from environment.utils import Location, Cell

class Environment:

    """
    Class to represent the environment of the path-finder.
    Attributes:
        length: Length of the grid. 
        breadth: Breadth of the grid.
        grid: Two-dimensional array of Cells representing the grid.
        heuristic: Heuristic function for guided algorithms.
        allowDiagonals: Whether diagonal movement of agents is possible.
        cutCorners: Whether agents are allowed to cut corners of walls.
    Methods:
        update: 
        idaupdate: 
        getActivatedCells: 
        getActivatedCells_IDA: 
        getPaths: 
        getJpsPaths: 
        getIDAPath: 
        bestHeuristic: 
        distance: 
    """

    def __init__(self, config, agents):

        """
        Constructor for class Environment.
        Arguments:
            config: Dictionary with all the configuration settings.
            agents: List of agents on the grid.
        """

        # Extract and initialise all the environment properties
        self.length = len(config['maze'])
        self.breadth = len(config['maze'][0])
        self.grid = [[Cell(Location(x, y)) for y in range(self.breadth)]
                     for x in range(self.length)]
        heuristicDict = {0: 'manhattan', 1: 'euclidean', 2: 'octile', 3: 'chebyshev'}
        self.heuristic = heuristicDict[int(config['heuristic'])]
        self.allowDiagonals = int(config['allowDiagonals'])
        self.cutCorners = int(config['cutCorners'])

        # Set up walls and cell weights
        for row in self.grid:
            for cell in row:
                if config['maze'][cell.location.x][cell.location.y] == 1:
                    cell.type = 'wall'
                else:
                    cell.weight = (100 - config['weights'][cell.location.x][cell.location.y]) / 100
                    cell.weight *= 2

        # Set up wormholes
        if 'wormhole' in config:
            wormhole = config['wormhole']
            x1, y1, x2, y2 = wormhole[0]['x'], wormhole[0]['y'], wormhole[1]['x'], wormhole[1]['y']
            if x1!=x2 or y1!=y2:
                wormholeEntry = self.grid[x1][y1]
                wormholeExit = self.grid[x2][y2]
                wormholeEntry.location.neighbours = [[x2, y2]]
                wormholeEntry.type = 'wormholeEntry'
                wormholeExit.type = 'wormholeExit'

        # Iterate over all agents, and mark them as either sources or destinations
        for agent in agents:
            x = agent.location.x
            y = agent.location.y
            self.grid[x][y].type = agent.type
            if agent.type == 'source':
                self.grid[x][y].srcAgent = agent
            else:
                self.grid[x][y].destAgent = agent
        

    # Import member functions
    from environment.heuristics import bestHeuristic, distance
    from environment.drawPath import getPath, getJpsPath, getIDAPath
    from environment.updateGrid import update, idaupdate, getActivatedCells, getActivatedCells_IDA

    # For debugging
    def print(self):
        for row in self.grid:
            for cell in row:
                if cell.type == 'waitList':
                    print('i', end=' ')
                else:
                    print(cell.type[0], end=' ')
            print()
        print()

    # For debugging
    def printInitial(self):
        for row in self.grid:
            for cell in row:
                if(cell.type == 'wall'):
                    print('#', end='')
                elif(cell.type == 'destination'):
                    print('X', end='')
                elif(cell.type == 'source'):
                    print('O', end='')
                else:
                    print('.', end='')
            print()
        print()
    
