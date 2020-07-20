import heapq


def dynamicAStar(self, environment, targets, relaxation, maxDepth):
    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [((1 + relaxation) * environment.bestHeuristic(
            sourceCell, targets), sourceCell, 0)]
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    minElement = heapq.heappop(self.waitList)
    nextCell = minElement[1]
    depth = minElement[2]
    self.visited.add(nextCell)
    self.logs.append([self, nextCell, 'visited'])

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nextCell, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        # newDistance = self.distances[nextCell] + neighbour.weight
        newDistance = self.distances[nextCell] + environment.distance(nextCell, neighbour)
        fValue = newDistance + (1 + relaxation - (relaxation * depth) / maxDepth ) * environment.bestHeuristic(neighbour, targets)
        if neighbour in self.distances and self.distances[neighbour] <= newDistance:
            continue
        self.distances[neighbour] = newDistance
        heapq.heappush(self.waitList, (fValue, neighbour, depth + 1))
        self.path[neighbour] = nextCell
        self.logs.append([self, neighbour, 'waitList'])
