from environment.utils import Location, Cell

class Environment:

    """
    Class to represent the environment of the path-finder.
    Attributes:
        length: Length of the grid. 
        breadth: Breadth of the grid.
        grid: Two-dimensional array of Cells representing the grid.
        heuristic: Heuristic function for informed algorithms.
        allowDiagonals: Whether diagonal movement of agents is possible.
        cutCorners: Whether agents are allowed to cut corners of walls.
    Methods:
        update: Updates states of grid cells.
        idaUpdate: Updates states of grid cells during IDA*.
        getActivatedCells: Returns list of activated cells in the environment.
        getActivatedCells_IDA: Returns list of activated cells in the environment during IDA*.
        getPath: Gets the final path from source to destination.
        getJpsPath: Gets the final path from source to destination for jump point search.
        getIDAPath: Gets the final path from source to destination for IDA*.
        bestHeuristic: Returns best heuristic from source to any destination.
        distance: Returns cost of travelling from one cell to another.
    """

    def __init__(self, config, agents):

        """
        Constructor for class Environment.
        Args:
            config: Dictionary with all the configuration settings.
            agents: List of agents on the grid.
        """

        # Extract and initialise all the environment properties
        self.length = len(config['maze'])
        self.breadth = len(config['maze'][0])
        self.grid = [[Cell(Location(x, y)) for y in range(self.breadth)]
                     for x in range(self.length)]
        self.allowDiagonals = int(config['allowDiagonals'])
        self.cutCorners = int(config['cutCorners'])
        
        if 'heuristic' in config:
            heuristicDict = {0: 'manhattan', 1: 'euclidean', 2: 'octile', 3: 'chebyshev'}
            self.heuristic = heuristicDict[int(config['heuristic'])]

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
    from environment.updateGrid import update, idaUpdate, getActivatedCells, getActivatedCells_IDA
    