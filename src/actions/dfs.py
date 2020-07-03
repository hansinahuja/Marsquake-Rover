from collections import deque

def dfs(self, environment):

    self.logs = []

    # First iteration
    if self.waitList == None:
        self.waitList = deque()
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList.append(sourceCell)
        # self.visited.add(sourceCell)

    # Exhausted all possible moves
    if len(self.waitList)==0:
        return

    nextCell = self.waitList.pop()
    if nextCell not in self.visited:
        self.visited.add(nextCell)
        self.logs.append([self, nextCell, 'visited'])

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        self.waitList.append(neighbour)
        self.path[neighbour] = nextCell
        # self.visited.add(neighbour)
        self.logs.append([self, neighbour, 'waitList'])