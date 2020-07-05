import heapq


def dijkstra(self, environment):

    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [(0, sourceCell)]
        self.distances[sourceCell] = 0
    # self.visited.add(sourceCell)

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    minElement = heapq.heappop(self.waitList)
    nextCell = minElement[1]
    self.visited.add(nextCell)
    self.logs.append([self, nextCell, 'visited'])
    # print(nextCell.location.x, nextCell.location.y, 'visited')

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        newDistance = self.distances[nextCell] + neighbour.weight
        if neighbour in self.distances and self.distances[neighbour] <= newDistance:
            continue
        heapq.heappush(self.waitList, (newDistance, neighbour))
        # self.waitList.put(neighbour)
        self.path[neighbour] = nextCell
        # self.visited.add(neighbour)
        self.distances[neighbour] = newDistance
        self.logs.append([self, neighbour, 'waitList'])
        # print(neighbour.location.x, neighbour.location.y, 'inQueue')
