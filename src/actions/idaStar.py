from collections import deque


# def reset(self, environment):


def idaStar(self, environment, threshold, targets):
    def valid(x, y):
        return x >= 0 and y >= 0 and x < environment.length and y < environment.breadth and environment.grid[x][y].type != 'wall'

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
    fValue = weight + environment.bestHeuristic(nextCell, targets)
    if fValue > threshold:
        if nextCell in self.visited and self.visited[nextCell] == 'inRecursion':
            self.visited[nextCell] = 'outOfRecursion'
            self.logs.append([self, nextCell, 'outOfRecursion'])
        if nextCell in self.visited and self.visited[nextCell] == 'visited':
            self.visited[nextCell] = 'free'
            self.logs.append([self, nextCell, 'free'])
        return fValue, weight
    
    self.logs.append([self, nextCell, 'visited'])
    
    for nx, ny in nextCell.location.neighbours:
        if not valid(nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        self.visited[nextCell] = 'inRecursion'
        self.waitList.append( (neighbour, weight + neighbour.weight) )
        self.path[(neighbour, weight + neighbour.weight)] = (nextCell, weight)
        self.distances[neighbour] = self.distances[nextCell] + neighbour.weight
    
    return fValue, weight