from math import sqrt
from environment.utils import Location

def bestHeuristic(self, source, destinations):
    minHeuristic = self.length + self.breadth
    for destination in destinations:
        minHeuristic = min(minHeuristic, heuristic(source, destination, self.heuristic))
    return minHeuristic


def heuristic(cellA, cellB, heuristic):
    deltaX = abs(cellA.location.x - cellB.location.x)
    deltaY = abs(cellA.location.y - cellB.location.y)
    if heuristic == 'manhattan':
        return manhattanDistance(deltaX, deltaY)
    elif heuristic == 'euclidean':
        return euclideanDistance(deltaX, deltaY)
    elif heuristic == 'octile':
        return octileDistance(deltaX, deltaY)
    elif heuristic == 'chebyshev':
        return chebyshevDistance(deltaX, deltaY)


def manhattanDistance(deltaX, deltaY):
    return deltaX + deltaY

def euclideanDistance(deltaX, deltaY):
    return sqrt(deltaX**2 + deltaY**2)

def octileDistance(deltaX, deltaY):
    return sqrt(2) * min(deltaX, deltaY) + abs(deltaX - deltaY)
    
def chebyshevDistance(deltaX, deltaY):
    return max(deltaX, deltaY)
