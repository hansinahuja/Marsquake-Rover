from collections import deque


# def reset(self, environment):


def ida(self, environment, threshold, targets):
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
        return True

    self.logs = []

    # first iteration
    if self.waitList == None:
        self.waitList = deque()
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList.append( (sourceCell, 0) )
        self.visited = {}
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return -1
    nextCell = self.waitList[-1][0]
    weight = self.waitList[-1][1]
    self.waitList.pop()
    
    if weight > threshold:
        if nextCell in self.visited and self.visited[nextCell] == 'inRecursion':
            self.visited[nextCell] = 'outOfRecursion'
            self.logs.append([self, nextCell, 'outOfRecursion'])
        if nextCell in self.visited and self.visited[nextCell] == 'visited':
            self.visited[nextCell] = 'free'
            self.logs.append([self, nextCell, 'free'])
        return weight, weight
    
    self.logs.append([self, nextCell, 'inRecursion'])
    
    for nx, ny in nextCell.location.neighbours:
        if not valid(nextCell, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        parent = nextCell
        if (nextCell, weight) in self.path:
            parent = self.path[(nextCell, weight)][0]
        neighbour = environment.grid[nx][ny]
        if neighbour == parent:
            continue
        self.visited[nextCell] = 'inRecursion'
        self.waitList.append( (neighbour, weight + neighbour.weight) )
        self.path[(neighbour, weight + neighbour.weight)] = (nextCell, weight)
        self.distances[neighbour] = self.distances[nextCell] + neighbour.weight
    
    return weight, weight