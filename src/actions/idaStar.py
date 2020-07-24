from collections import deque

def idaStar(self, environment, threshold, targets):
    
    """
    Performs one iteration of ida* based on agent's current state and threshold.
    Args:
        environment: The current environment
        targets: The target agents
        threshold: Maximum permissible f value.
    """

    # Helper function to check if location is valid
    def valid(currentCell, x2, y2):
        x1, y1 = currentCell.location.x, currentCell.location.y
        if x2 < 0 or x2 >= environment.length or y2 < 0 or y2 >= environment.breadth:
            return False
        nextCell = environment.grid[x2][y2]
        if nextCell.type == 'wall':
            return False
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

    # Clean the logs
    self.logs = []

    # First iteration
    if self.waitList == None:
        self.waitList = deque()
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList.append( (sourceCell, 0) )
        self.visited = {}
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return -1, -1

    # Pop the top element and log the changes
    nextCell = self.waitList[-1][0]
    weight = self.waitList[-1][1]
    self.waitList.pop()
    fValue = weight + environment.bestHeuristic(nextCell, targets)

    # Check if f value is within threshold
    if fValue > threshold:
        if nextCell in self.visited and self.visited[nextCell] == 'inRecursion':
            self.visited[nextCell] = 'outOfRecursion'
            self.logs.append([self, nextCell, 'outOfRecursion'])
        if nextCell in self.visited and self.visited[nextCell] == 'visited':
            self.visited[nextCell] = 'free'
            self.logs.append([self, nextCell, 'free'])
        return fValue, weight
    
    self.logs.append([self, nextCell, 'visited'])
    nextCell.srcAgent = self
    path = environment.getIDAPath(nextCell)
    # Iterate over valid neighbours
    for nx, ny in nextCell.location.neighbours:
        if not valid(nextCell, nx, ny):
            continue
        point = {'x': nx, 'y': ny}
        if point in path:
            continue
        parent = nextCell
        if (nextCell, weight) in self.path:
            parent = self.path[(nextCell, weight)][0]
        neighbour = environment.grid[nx][ny]
        if neighbour == parent:
            continue
        
        # Add the neighbour to the queue and log the changes
        self.visited[nextCell] = 'inRecursion'
        self.waitList.append( (neighbour, weight + environment.distance(nextCell, neighbour)) )
        self.path[(neighbour, weight + environment.distance(nextCell, neighbour))] = (nextCell, weight)
        self.distances[neighbour] = self.distances[nextCell] + environment.distance(nextCell, neighbour)
    
    return fValue, weight
