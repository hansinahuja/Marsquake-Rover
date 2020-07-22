from math import sqrt

def distance(self, src, dest):

    """
    Returns cost of travelling from one cell to another.
    Args:
        src: Source cell.
        dest: Destination cell.
    Returns:
        Cost of travelling from src to dest.
    """

    # Cost of taking a wormhole = 0
    if src.type == 'wormholeEntry' and dest.type=='wormholeExit':
        return 0

    deltaX = abs(src.location.x - dest.location.x)
    deltaY = abs(src.location.y - dest.location.y)
    return dest.weight * sqrt(manhattanDistance(deltaX, deltaY))

def bestHeuristic(self, source, destinations):

    """
    Returns best heuristic from source to any destination.
    Args:
        source: Source cell.
        destinations: List of destination cells.
    Returns:
        minHeuristic: Best source to destination heuristic.
    """

    minHeuristic = self.length + self.breadth
    for destination in destinations:
        minHeuristic = min(minHeuristic, heuristic(source, destination, self.heuristic))
    return minHeuristic


def heuristic(src, dest, heuristic):

    """
    Returns heuristic from source to destination.
    Args:
        src: Source cell.
        dest: Destination cell.
        heuristic: Heuristic choice.
    Returns:
        Distance between src and dest based on selected heuristic.
    """

    deltaX = abs(src.location.x - dest.location.x)
    deltaY = abs(src.location.y - dest.location.y)
    if heuristic == 'manhattan':
        return manhattanDistance(deltaX, deltaY)
    elif heuristic == 'euclidean':
        return euclideanDistance(deltaX, deltaY)
    elif heuristic == 'octile':
        return octileDistance(deltaX, deltaY)
    elif heuristic == 'chebyshev':
        return chebyshevDistance(deltaX, deltaY)


# Helper functions to calculate heuristics
def manhattanDistance(deltaX, deltaY):
    return deltaX + deltaY

def euclideanDistance(deltaX, deltaY):
    return sqrt(deltaX**2 + deltaY**2)

def octileDistance(deltaX, deltaY):
    return sqrt(2) * min(deltaX, deltaY) + abs(deltaX - deltaY)
    
def chebyshevDistance(deltaX, deltaY):
    return max(deltaX, deltaY)
