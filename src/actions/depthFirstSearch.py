from collections import deque


def depthFirstSearch(self, environment):

    self.logs = []

    # First iteration
    if self.waitList == None:
        self.waitList = deque()
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList.append(sourceCell)
        self.visited = {}

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    nextCell = self.waitList[-1]
    if nextCell in self.visited:
        self.waitList.pop()
        if self.visited[nextCell] == 'inRecursion':
            self.visited[nextCell] = 'outOfRecursion'
            self.logs.append([self, nextCell, 'outOfRecursion'])
            # print(nextCell.location.x, nextCell.location.y, 'outOfRecursion')
        self.logs.append(None)
        return

    self.visited[nextCell] = 'inRecursion'
    self.logs.append([self, nextCell, 'inRecursion'])
    # print(nextCell.location.x, nextCell.location.y, 'inRecursion')

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        self.waitList.append(neighbour)
        self.path[neighbour] = nextCell