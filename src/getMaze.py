from agent import Agent
import random
from environment.env import Environment
from environment.utils import Location

def getMaze(dict):
    
    """
    Creates a random maze.
    Args:
        dict: Dictionary for the dimensions of maze and the algorithm to be used.
    Returns:
        walls: Walls placed by the algorithm.
        source: Position of a free cell to place source.
        destination: Position of a free cell to place destination.
    """
    
    length = int(dict['length'])
    breadth = int(dict['breadth'])

    maze = [ [ int(0) for i in range(breadth) ] for j in range(length) ]
    weights = [ [ int(50) for i in range(breadth) ] for j in range(length) ]

    config = {'maze': maze,
              'weights': weights,
              'allowDiagonals': 0,
              'cutCorners': 0,
              'heuristic': 0
            }

    if int(dict['algo']) == 0:
        return recursiveMaze(config)
    else:
        return randomizedPrim(config)

def recursiveMaze(dict):
    
    """
    Creates a random maze.
    Args:
        dict: Dictionary with all the configuration settings.
    Returns:
        walls: Walls placed by the algorithm.
        source: Position of a free cell to place source.
        destination: Position of a free cell to place destination.
    """

    # Intialize the environment
    env = Environment(dict, [])

    def generate(left, right, top, bottom):
        if left >= right or top >= bottom:
            return
        if left >= right - 1 and top >= bottom - 1:
            return

        rnd = random.randrange(0, 2)   
        if left >= right - 1:
            rnd = 0
        if top >= bottom - 1:
            rnd = 1

        # Horizontally divide the grid
        if(rnd == 0):                                                 
            row = randomEvenNumber(top, bottom)
            for i in range(left, right + 1):
                if env.grid[row][i].type != 'source' and env.grid[row][i].type != 'destination':
                    env.grid[row][i].type = 'wall'
            i = randomOddNumber(left, right)
            if env.grid[row][i].type != 'source' and env.grid[row][i].type != 'destination':
                env.grid[row][i].type = 'free'                    
            generate(left, right, top, row - 1)
            generate(left, right, row + 1, bottom)
        
        # Vertically divide the grid
        else:                                                           
            clm = randomEvenNumber(left, right)
            for i in range(top, bottom + 1):
                if env.grid[i][clm].type != 'source' and env.grid[i][clm].type != 'destination':
                    env.grid[i][clm].type = 'wall'
        
            i = randomOddNumber(top, bottom)
            if env.grid[i][clm].type != 'source' and env.grid[i][clm].type != 'destination':
                env.grid[i][clm].type = 'free'          
            generate(left, clm - 1, top, bottom)
            generate(clm + 1, right, top, bottom)

    generate(0, env.breadth - 1, 0, env.length - 1)
    gridChanges = []
    flag = 1

    # Append grid changes
    for row in env.grid:
        count = 0
        for cell in row:
            count += 1
            if cell.type == 'wall':
                gridChange = {'x': cell.location.x,
                            'y': cell.location.y}
                gridChanges.append(gridChange)
            else:
                dst = {'x': cell.location.x,
                    'y': cell.location.y}
                if flag and count > 2:
                    flag = 0
                    src = {'x': cell.location.x,
                        'y': cell.location.y}
    
    return {'walls':gridChanges, 'source':src, 'destination':dst}


def randomizedPrim(dict) :
    
    """
    Creates a random maze.
    Args:
        dict: Dictionary with all the configuration settings.
    Returns:
        walls: Walls placed by the algorithm.
        source: Position of a free cell to place source.
        destination: Position of a free cell to place destination.
    """

    # Intialize environment
    env = Environment(dict, [])
    
    # Initialize the grid as all walls and find a start cell
    for row in env.grid:
        for cell in row:
            if cell.type != 'source' and cell.type != 'destination':
                cell.type = 'wall'
                src = cell
    cell.type = 'free'
    blocked = getBlockedCells(src, env)
    
    while len(blocked) :
        cell = blocked.pop()
        free = getFreeCells(cell, env)
        newFree = mid(free, cell, env)
        if newFree.type == 'wall':
            newFree.type = 'free'
        if cell.type == 'wall':
            cell.type = 'free'
        S1 = getBlockedCells(cell, env)
        for i in S1:
            blocked.add(i)
    
    # Append grid changes
    gridChanges = []
    flag = 1
    for row in env.grid:
        count = 0
        for cell in row:
            count += 1
            if cell.type == 'wall':
                gridChange = {'x': cell.location.x,
                            'y': cell.location.y}
                gridChanges.append(gridChange)
            else:
                dst = {'x': cell.location.x,
                    'y': cell.location.y}
                if flag and count > 2:
                    flag = 0
                    src = {'x': cell.location.x,
                        'y': cell.location.y}

    return {'walls':gridChanges, 'source':src, 'destination':dst}

# Helper functions 
def randomOddNumber(low, high):
    low = low // 2 
    if high % 2:
        high = high // 2
    else:
        high = high // 2 - 1
    return 2 * random.randrange(low, high+1) + 1

def randomEvenNumber(low, high):
    low = low // 2 + low % 2
    high = high // 2 
    return 2 * random.randrange(low, high+1)

def isValid(x, y, env):
    return x >=0 and y>=0 and x < env.length and y < env.breadth

def mid(cellA, cellB, env):
    return env.grid[ (cellA.location.x + cellB.location.x) // 2][ (cellA.location.y + cellB.location.y) // 2 ]
 
def getBlockedCells(cell, env):
    x = cell.location.x
    y = cell.location.y
    dx = [0, 2, 0, -2]
    dy = [-2, 0, 2, 0]
    ret = set()
    for i in range(4):
        X = x + dx[i]
        Y = y + dy[i]
        if isValid(X, Y, env) and env.grid[X][Y].type == 'wall':
            ret.add( env.grid[X][Y] )
    return ret
def getFreeCells(cell, env):
    x = cell.location.x
    y = cell.location.y
    dx = [0, 2, 0, -2]
    dy = [-2, 0, 2, 0]
    ret = set()
    for i in range(4):
        X = x + dx[i]
        Y = y + dy[i]
        if isValid(X, Y, env) and env.grid[X][Y].type != 'wall':
            ret.add( env.grid[X][Y] )
    return ret.pop()