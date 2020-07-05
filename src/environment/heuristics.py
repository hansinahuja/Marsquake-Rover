from math import sqrt
from environment.utils import Location

def bestHeuristic(self, source, destinations):
    minHeuristic = self.length + self.breadth
    for destination in destinations:
        minHeuristic = min(minHeuristic, heuristic(source, destination, self.heuristic))
    return minHeuristic


def heuristic(cellA, cellB, heuristic):
    pointA = Location(cellA.location.x, cellA.location.y)
    pointB = Location(cellB.location.x, cellB.location.y)
    if heuristic == 'manhattan':
        return manhattanDistance(pointA, pointB)
    elif heuristic == 'euclidean':
        return euclideanDistance(pointA, pointB)
    elif heuristic == 'octile':
        return octileDistance(pointA, pointB)
    elif heuristic == 'chebyshev':
        return chebyshevDistance(pointA, pointB)


def manhattanDistance(pointA, pointB):
    return abs(pointA.x - pointB.x) + abs(pointA.y - pointB.y)

def euclideanDistance(pointA, pointB):
    return sqrt((pointA.x - pointB.x)**2 + (pointA.y - pointB.y)**2)

def octileDistance(pointA, pointB):
    deltaX = abs(pointA.x - pointB.x)
    deltaY = abs(pointA.y - pointB.y)
    return 1.414 * min(deltaX, deltaY) + abs(deltaX - deltaY)
    
def chebyshevDistance(pointA, pointB):
    return max(abs(pointA.x - pointB.x), abs(pointA.y - pointB.y))
