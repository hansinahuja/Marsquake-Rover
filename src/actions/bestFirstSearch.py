import heapq


def bestFirstSearch(self, environment, targets):

    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [(environment.bestHeuristic(
            sourceCell, targets), sourceCell)]

    if len(self.waitList) == 0:
        return

    minElement = heapq.heappop(self.waitList)
    nextCell = minElement[1]
    self.visited.add(nextCell)
    self.logs.append([self, nextCell, 'visited'])
    # print(nextCell.location.x, nextCell.location.y, 'visited')

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nextCell, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        heuristic = environment.bestHeuristic(neighbour, targets)
        heapq.heappush(self.waitList, (heuristic, neighbour))
        self.path[neighbour] = nextCell
        # self.visited.add(neighbour)
        self.logs.append([self, neighbour, 'waitList'])
        # print(neighbour.location.x, neighbour.location.y, 'inQueue')
