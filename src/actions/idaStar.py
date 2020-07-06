from collections import deque


# def reset(self, environment):


def idaStar(self, environment, threshold, targets):

    self.logs = []

    # first iteration
    if self.waitList == None:
        self.waitList = deque()
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList.append(sourceCell)
        self.visited = {}
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return -1

    nextCell = self.waitList[-1]
    fValue = self.distances[nextCell] + environment.bestHeuristic(nextCell, targets)
    if nextCell in self.visited:
        self.waitList.pop()
        if self.visited[nextCell] == 'inRecursion':
            self.visited[nextCell] = 'outOfRecursion'
            self.logs.append([self, nextCell, 'outOfRecursion'])
            # print(nextCell.location.x, nextCell.location.y, 'outOfRecursion')
        return fValue

    if fValue > threshold:
        self.waitList.pop()
        if nextCell in self.visited and self.visited[nextCell] == 'inRecursion':
            self.visited[nextCell] = 'outOfRecursion'
            self.logs.append([self, nextCell, 'outOfRecursion'])
        return fValue
    
    self.visited[nextCell] = 'inRecursion'
    self.logs.append([self, nextCell, 'inRecursion'])

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        self.waitList.append(neighbour)
        self.path[neighbour] = nextCell
        self.distances[neighbour] = self.distances[nextCell] + neighbour.weight
    
    return fValue